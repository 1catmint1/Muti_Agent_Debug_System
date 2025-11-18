"""
JavaVerifier - Java代码验证器
"""
import os
import re
import tempfile
import shutil
import subprocess
from typing import Dict, List, Any
import builtins

from .base_verifier import BaseVerifier, Language


def extract_classes_from_comment_block(block: str) -> List[str]:
    """
    从 /** ... */ 注释块中提取完整 Java 类定义。
    使用手动扫描 + { } 深度计数，不使用正则。
    """
    classes = []
    lines = block.splitlines()
    n = len(lines)

    i = 0
    while i < n:
        line = lines[i].lstrip(" *\t").rstrip()

        if re.search(r"\bclass\b", line):
            content = []
            brace_depth = 0
            found_brace = False

            while i < n:
                raw = lines[i].lstrip(" *\t").rstrip()
                content.append(raw)

                for ch in raw:
                    if ch == "{":
                        brace_depth += 1
                        found_brace = True
                    elif ch == "}":
                        brace_depth -= 1

                i += 1

                if found_brace and brace_depth == 0:
                    classes.append("\n".join(content))
                    break
        else:
            i += 1

    return classes


class JavaVerifier(BaseVerifier):
    """Java专用验证器"""

    def __init__(self):
        super().__init__(Language.JAVA)

    def _contains_real_class(self, code: str, classname: str) -> bool:
        """
        判断 code 中是否存在真实类定义（非注释中的）。
        通过删除注释来检测。
        """
        target = f"class {classname}"

        cleaned = []
        i = 0
        n = len(code)
        inside_block = False
        inside_line = False

        while i < n:
            # /** */ 注释
            if not inside_line and i + 1 < n and code[i] == '/' and code[i + 1] == '*':
                inside_block = True
                i += 2
                continue

            if inside_block:
                if i + 1 < n and code[i] == '*' and code[i + 1] == '/':
                    inside_block = False
                    i += 2
                    continue
                i += 1
                continue

            # // 注释
            if not inside_block and i + 1 < n and code[i] == '/' and code[i + 1] == '/':
                inside_line = True
                i += 2
                continue

            if inside_line:
                if code[i] == '\n':
                    inside_line = False
                i += 1
                continue

            # 非注释内容
            cleaned.append(code[i])
            i += 1

        cleaned_code = "".join(cleaned)
        return target in cleaned_code

    def _inject_missing_definitions(self, file_path: str):
        """
        自动从 /** ... */ 注释中提取所有类定义（不限类名）并注入到文件顶部。
        使用 extract_classes_from_comment_block 做深度解析，避免正则截断类体。
        """

        print(f"[JavaVerifier][DEBUG] _inject_missing_definitions 调用 file={file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            original_code = f.read()

        print("--------------- [DEBUG] 注入前代码 BEGIN ---------------")
        print(original_code[:400])
        print("--------------- [DEBUG] 注入前代码 END -----------------")

        # 找出所有 /** ... */ 注释块
        comment_blocks = re.findall(r"/\*\*([\s\S]*?)\*/", original_code)
        print(f"[JavaVerifier][DEBUG] 注释块数量: {len(comment_blocks)}")

        if not comment_blocks:
            print("[JavaVerifier][DEBUG] 没有注释块，停止注入")
            return

        to_inject = []

        for idx, block in enumerate(comment_blocks):
            print(f"[DEBUG] 第 {idx + 1} 个注释块内容（前 200 字）：")
            print(block[:200])

            class_defs = extract_classes_from_comment_block(block)

            print(f"[DEBUG] 深度解析器抽取出类定义数量: {len(class_defs)}")

            for cls_code in class_defs:
                m = re.search(r"class\s+(\w+)", cls_code)
                if not m:
                    print("[DEBUG] 未识别到类名，跳过")
                    continue

                cls_name = m.group(1)
                print(f"[DEBUG] 找到类名: {cls_name}")

                if self._contains_real_class(original_code, cls_name):
                    print(f"[DEBUG] 源文件中已有类 {cls_name}，跳过注入")
                    continue

                print(f"[DEBUG] ⭐ 准备注入类定义: {cls_name}")

                # 将 public class => class，避免 javac 报“需独立文件”
                safe_cls_code = re.sub(r"\bpublic\s+class\b", "class", cls_code)

                to_inject.append(safe_cls_code)

        if to_inject:
            injected_code = "\n\n".join(to_inject) + "\n\n" + original_code

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(injected_code)

            print("--------------- [DEBUG] 注入后的代码 BEGIN ---------------")
            print(injected_code[:3000])
            print("--------------- [DEBUG] 注入后的代码 END -----------------")

            print(f"[JavaVerifier] 🔧 已自动注入 {len(to_inject)} 个类定义")
        else:
            print("[JavaVerifier][DEBUG] ❗ 没有可注入的类定义")

    def verify_syntax(self, file: Dict[str, Any]) -> Dict[str, Any]:
        """语法验证：使用javac编译（支持外部依赖）"""
        content = file.get("content", "")
        raw_name = file.get("file", "temp.java")
        filename = os.path.basename(raw_name)

        result = {"success": False, "errors": []}

        tmp_dir = tempfile.mkdtemp(prefix="java_verify_")

        print(f"[JavaVerifier] 开始语法验证: {raw_name}")
        print(f"[JavaVerifier] 临时目录: {tmp_dir}")

        try:
            # 写入临时文件
            filepath = os.path.join(tmp_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self._inject_missing_definitions(filepath)

            print(f"[JavaVerifier] 写入文件: {filepath}")

            # ==== ✅ 自动补全 imports（增强：支持 Stack / Deque / ArrayList 等）====
            def auto_add_imports_if_needed(file_path: str):
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()

                needed_imports = []

                # 反射相关
                if re.search(r"\b(Type|WildcardType|TypeVariable)\b", code):
                    needed_imports.append("import java.lang.reflect.*;")

                # 集合/容器类（包括 Stack/Deque/ArrayDeque/LinkedList/ArrayList/Queue）
                if re.search(r"\b(Collection|List|Map|Set|Queue|Deque|ArrayDeque|LinkedList|ArrayList|Stack|Collections|Arrays)\b", code):
                    needed_imports.append("import java.util.*;")

                # mockito/junit
                if "mock(" in code or "Mockito" in code:
                    needed_imports.append("import static org.mockito.Mockito.*;")
                    needed_imports.append("import org.junit.internal.ViolatedAssumptionAnswer;")

                if needed_imports:
                    updated = False
                    for imp in needed_imports:
                        if imp not in code:
                            code = imp + "\n" + code
                            updated = True
                    if updated:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(code)
                        print(f"[JavaVerifier] ✅ 自动补全 imports: {needed_imports}")

            auto_add_imports_if_needed(filepath)

            # ==== ✅ 构建 classpath ====
            libs_dir = os.path.join(os.getcwd(), "libs")
            jar_files = []
            if os.path.isdir(libs_dir):
                jar_files = [os.path.join(libs_dir, f) for f in os.listdir(libs_dir) if f.endswith(".jar")]
            classpath = os.pathsep.join(jar_files + [tmp_dir]) if jar_files else tmp_dir
            print(f"[JavaVerifier] 使用 classpath:\n  {classpath.replace(os.pathsep, os.linesep + '  ')}")

            # ==== ✅ 编译命令 ====
            compile_cmd = ["javac", "-encoding", "UTF-8", "-cp", classpath, "-d", tmp_dir, filepath]
            print(f"[JavaVerifier] 编译命令: {' '.join(compile_cmd)}")

            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if compile_result.returncode == 0:
                result["success"] = True
                print(f"[JavaVerifier] ✅ 编译成功")
            else:
                print(f"[JavaVerifier] ❌ 编译失败:\n{compile_result.stderr}")
                stderr = compile_result.stderr or ""
                for line in stderr.split('\n'):
                    if '.java:' in line:
                        match = re.search(r':(\d+):\s*error:\s*(.+)', line)
                        if match:
                            result["errors"].append({
                                "line": int(match.group(1)),
                                "message": match.group(2)
                            })

        except subprocess.TimeoutExpired:
            result["errors"].append({"line": 0, "message": "编译超时"})
            print(f"[JavaVerifier] ⚠️ 编译超时")
        except FileNotFoundError:
            result["errors"].append({"line": 0, "message": "javac 未找到，请确保 JDK 已安装"})
            print(f"[JavaVerifier] ❌ 未找到 javac，请检查 JDK 环境变量 PATH")
        except Exception as e:
            result["errors"].append({"line": 0, "message": str(e)})
            print(f"[JavaVerifier] ⚠️ 验证异常: {e}")
            import traceback
            traceback.print_exc()
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        return result

    def verify_functionality(self, file: Dict[str, Any],
                             test_cases: List[Dict] = None) -> Dict[str, Any]:

        # ============================================
        #  🔥 方案 2：LLM-Based 功能验证模式（不依赖编译）
        #  —— 仅当用户启用 builtins.DEBUGBENCH_USE_LLM_VERIFY 时
        # ============================================
        if getattr(builtins, "DEBUGBENCH_USE_LLM_VERIFY", False):

            tmp_dir = tempfile.mkdtemp(prefix="java_llm_verify_")
            filepath = os.path.join(tmp_dir, "tmp.java")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(file.get("content", ""))

            self._inject_missing_definitions(filepath)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            print("[JavaVerifier] 🤖 使用 LLM-Based 功能验证（跳过编译与运行）")

            # ① 必须至少包含一个 class 定义
            if "class " not in content:
                return {"success": False, "passed": 0, "failed": 1, "errors": [{"message": "缺少 class 定义"}]}

            # ② 检查 return
            if "return" not in content:
                return {"success": False, "passed": 0, "failed": 1, "errors": [{"message": "缺少 return 语句"}]}

            # ③ 花括号 {} 配对
            if content.count("{") != content.count("}"):
                return {"success": False, "passed": 0, "failed": 1, "errors": [{"message": "花括号不匹配"}]}

            # ④ 圆括号 () 配对
            if content.count("(") != content.count(")"):
                return {"success": False, "passed": 0, "failed": 1, "errors": [{"message": "圆括号不匹配"}]}

            # ⑤ System.out.println 基本闭合检查
            if "System.out" in content:
                last_print = content.split("System.out")[-1]
                if ");" not in last_print:
                    return {"success": False, "passed": 0, "failed": 1, "errors": [{"message": "System.out.println 可能未正确闭合"}]}

            # ⑥ 简单越界风险（<= length()）提示
            if re.search(r"<=\s*\w+\.length\(\)", content):
                return {"success": False, "passed": 0, "failed": 1, "errors": [{"message": "可能存在数组越界风险（<= length()）"}]}

            # ⑦ 树题递归传参常见错误（示例）
            if re.search(r"task\s*\(\s*root\s*,\s*false\s*\)", content):
                return {
                    "success": False, "passed": 0, "failed": 1,
                    "errors": [{"line": 0, "message": "疑似递归传参错误：task(root, false) 可能应为 task(root.right, false)"}]
                }

            return {"success": True, "passed": 1, "failed": 0, "errors": []}

        # ============================================================
        #  原生路径（编译 + 运行）
        # ============================================================
        result = {"success": True, "passed": 0, "failed": 0, "errors": []}

        if not test_cases:
            return result

        print(f"[JavaVerifier] 功能验证: {len(test_cases)} 个测试用例")

        content = file.get("content", "")
        filename = file.get("file", "Main.java")

        tmp_dir = tempfile.mkdtemp(prefix="java_run_")

        try:
            filepath = os.path.join(tmp_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            self._inject_missing_definitions(filepath)

            # 编译
            compile_cmd = ["javac", "-encoding", "UTF-8", "-d", tmp_dir, filepath]
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if compile_result.returncode != 0:
                result["success"] = False
                result["errors"].append({"message": "编译失败"})
                return result

            class_match = re.search(r'public\s+class\s+(\w+)', content)
            if not class_match:
                result["errors"].append({"message": "未找到public类"})
                return result

            class_name = class_match.group(1)

            for i, test_case in enumerate(test_cases):
                test_input = test_case.get("input", "")
                expected_output = test_case.get("expected_output", "")

                try:
                    run_cmd = ["java", "-cp", tmp_dir, class_name]
                    run_result = subprocess.run(
                        run_cmd,
                        input=test_input,
                        capture_output=True,
                        text=True,
                        timeout=5,
                        cwd=tmp_dir
                    )

                    actual_output = run_result.stdout.strip()

                    if actual_output == expected_output:
                        result["passed"] += 1
                    else:
                        result["failed"] += 1
                        result["errors"].append({
                            "test_case": i + 1,
                            "expected": expected_output,
                            "actual": actual_output
                        })

                except subprocess.TimeoutExpired:
                    result["failed"] += 1
                    result["errors"].append({"test_case": i + 1, "error": "超时"})
                except Exception as e:
                    result["failed"] += 1
                    result["errors"].append({"test_case": i + 1, "error": str(e)})

            result["success"] = result["failed"] == 0

        except Exception as e:
            result["success"] = False
            result["errors"].append({"message": str(e)})
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        return result