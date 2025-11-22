# analyzers/java_scanner.py
"""
JavaScanner - Java代码扫描器
支持：PMD, Checkstyle, SpotBugs
"""
import os
import re
import json
import shutil
import tempfile
import subprocess
from typing import Dict, List, Any
from xml.etree import ElementTree as ET

from .base_scanner import BaseScanner, Finding, Language


class JavaScanner(BaseScanner):
    """Java专用扫描器"""

    def __init__(self, files: List[Dict[str, Any]]):
        super().__init__(files, Language.JAVA)

    def scan_builtin(self) -> List[Finding]:
        """内置规则扫描：检测常见Java问题"""
        findings = []

        for f in self.files:
            filename = f.get("file", "")
            content = f.get("content", "")
            if not content:
                continue

            lines = content.split('\n')

            # 规则1: 空catch块
            for i, line in enumerate(lines, 1):
                if re.search(r'catch\s*\([^)]+\)\s*\{\s*\}', line):
                    findings.append(Finding(
                        file=filename,
                        line=i,
                        column=0,
                        severity="MEDIUM",
                        rule_id="JAVA001",
                        message="空catch块：异常被吞掉，应至少记录日志",
                        snippet=line.strip()[:100],
                        language=self.language.value,
                        fix_suggestion="添加日志记录或重新抛出异常"
                    ))

            # 规则2: System.out.println 在生产代码中
            if "Test" not in filename and "test" not in filename.lower():
                for i, line in enumerate(lines, 1):
                    if "System.out.print" in line and not line.strip().startswith("//"):
                        findings.append(Finding(
                            file=filename,
                            line=i,
                            column=0,
                            severity="LOW",
                            rule_id="JAVA002",
                            message="使用System.out.print输出，应使用日志框架",
                            snippet=line.strip()[:100],
                            language=self.language.value,
                            fix_suggestion="替换为logger.info()或logger.debug()"
                        ))

            # 规则3: == 比较字符串
            for i, line in enumerate(lines, 1):
                if re.search(r'\w+\s*==\s*"[^"]*"', line) or re.search(r'"[^"]*"\s*==\s*\w+', line):
                    if not line.strip().startswith("//"):
                        findings.append(Finding(
                            file=filename,
                            line=i,
                            column=0,
                            severity="HIGH",
                            rule_id="JAVA003",
                            message="使用==比较字符串，应使用.equals()方法",
                            snippet=line.strip()[:100],
                            language=self.language.value,
                            fix_suggestion="替换为str1.equals(str2)"
                        ))

            # 规则4: 未关闭的资源
            for i, line in enumerate(lines, 1):
                if re.search(
                        r'new\s+(FileReader|FileWriter|BufferedReader|BufferedWriter|FileInputStream|FileOutputStream|Scanner)\s*\(',
                        line):
                    context = '\n'.join(lines[max(0, i - 5):min(len(lines), i + 10)])
                    if 'try' not in context or 'finally' not in context:
                        findings.append(Finding(
                            file=filename,
                            line=i,
                            column=0,
                            severity="HIGH",
                            rule_id="JAVA004",
                            message="资源可能未正确关闭，建议使用try-with-resources",
                            snippet=line.strip()[:100],
                            language=self.language.value,
                            fix_suggestion="使用 try(Resource r = new Resource()) { ... }"
                        ))

            # 规则5: 空指针风险
            for i, line in enumerate(lines, 1):
                if re.search(r'\.\w+\s*\(', line) and 'if' not in line and 'null' in line:
                    findings.append(Finding(
                        file=filename,
                        line=i,
                        column=0,
                        severity="MEDIUM",
                        rule_id="JAVA005",
                        message="潜在的空指针异常风险",
                        snippet=line.strip()[:100],
                        language=self.language.value,
                        fix_suggestion="添加null检查或使用Optional"
                    ))

        return findings

    def scan_external(self, tool_config: Dict[str, bool] = None) -> List[Finding]:
        """外部工具扫描：PMD, Checkstyle"""
        if tool_config is None:
            tool_config = {
                "pmd": True,
                "checkstyle": False,  # 默认禁用（需要配置文件）
                "spotbugs": False,  # 默认禁用（需要编译）
            }

        findings: List[Finding] = []

        # 创建临时目录
        tmp_dir = tempfile.mkdtemp(prefix="java_scan_")
        try:
            # 写入文件：只用 basename，避免原始绝对路径导致 PMD 无法识别
            for f in self.files:
                raw_name = f.get("file", "") or f.get("path", "") or ""
                filename = os.path.basename(raw_name)
                content = f.get("content", "")

                if not filename.endswith(".java"):
                    continue

                filepath = os.path.join(tmp_dir, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                with open(filepath, 'w', encoding='utf-8') as fp:
                    fp.write(content)

            # PMD
            if tool_config.get("pmd", True):
                findings.extend(self._run_pmd(tmp_dir))

            # Checkstyle
            if tool_config.get("checkstyle", False):
                findings.extend(self._run_checkstyle(tmp_dir))

        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        return findings

    def _run_pmd(self, tmp_dir: str) -> List[Finding]:
        """运行PMD静态分析"""
        findings = []

        # --- 自动检测 Java/PMD 环境 ---
        import shutil

        # 1) 检查 java 是否可用
        if shutil.which("java") is None:
            print("❌ 未检测到 Java，请安装 JDK 并确保 java 在 PATH 中。")
            print("   参考安装：https://adoptium.net/ 或 Oracle JDK 17+")
            return findings

        # 2) 优先从环境变量中读取 PMD 路径（PMD_BIN 或 PMD_HOME）
        pmd_cmd = None
        pmd_home = os.environ.get("PMD_BIN") or os.environ.get("PMD_HOME")
        if pmd_home:
            # 例如 PMD_BIN=C:\tools\pmd\bin
            candidate = os.path.join(pmd_home, "pmd.bat" if os.name == "nt" else "pmd")
            if os.path.isfile(candidate):
                pmd_cmd = candidate

        # 3) 如果环境变量没有配置，再用 which 查找
        if pmd_cmd is None:
            pmd_cmd = shutil.which("pmd")

        if not pmd_cmd:
            print("❌ 未检测到 PMD。请确认：")
            print("   1) pmd 命令在当前 Python 进程的 PATH 中；或")
            print("   2) 设置环境变量 PMD_BIN 或 PMD_HOME 指向包含 pmd 可执行文件的目录。")
            return findings

        # --- 调试输出 PMD 命令和临时目录内容 ---
        print(f"[DEBUG] 使用 PMD 命令: {pmd_cmd}")
        print(f"[DEBUG] PMD 扫描目录: {tmp_dir}")
        for root, _, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith(".java"):
                    print(f"   -> {os.path.join(root, f)}")

        # --- 运行 PMD ---
        try:
            cmd = [pmd_cmd, "check", "-d", tmp_dir, "-f", "json", "-R", "category/java/errorprone.xml"]
            print(f"[DEBUG] 运行命令: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
            print(f"[DEBUG] PMD stdout 前500字:\n{result.stdout[:500]}")
            print(f"[DEBUG] PMD stderr 前200字:\n{result.stderr[:200]}")

            if not result.stdout.strip():
                print("⚠️ PMD 未输出任何结果，可能没有检测到问题或文件路径错误。")
                return findings

            # --- 解析 JSON ---
            try:
                data = json.loads(result.stdout)
                total = sum(len(f.get("violations", [])) for f in data.get("files", []))
                print(f"[DEBUG] ✅ 成功解析 PMD violations: 共 {total} 条")

                for file_data in data.get("files", []):
                    filename = os.path.basename(file_data.get("filename", ""))
                    for v in file_data.get("violations", []):
                        findings.append(Finding(
                            file=filename,
                            line=v.get("beginline", 0),
                            column=v.get("begincolumn", 0),
                            severity=self._map_pmd_severity(v.get("priority", 3)),
                            rule_id=f"PMD_{v.get('rule', 'UNKNOWN')}",
                            message=v.get("description", ""),
                            language=self.language.value,
                            tool="pmd"
                        ))
            except json.JSONDecodeError as e:
                print(f"⚠️ PMD 输出解析失败: {e}\n原始输出片段: {result.stdout[:200]}")

        except subprocess.TimeoutExpired:
            print("⚠️ PMD 执行超时")
        except Exception as e:
            print(f"⚠️ PMD 执行失败: {e}")

        return findings


    def _run_checkstyle(self, tmp_dir: str) -> List[Finding]:
        """运行Checkstyle代码风格检查"""
        findings = []
        # 实现类似PMD的逻辑
        # 由于需要checkstyle.jar和配置文件，这里暂时跳过
        return findings

    def _map_pmd_severity(self, priority: int) -> str:
        """映射PMD优先级到标准严重程度"""
        if priority == 1:
            return "HIGH"
        elif priority == 2:
            return "HIGH"
        elif priority == 3:
            return "MEDIUM"
        elif priority == 4:
            return "LOW"
        else:
            return "LOW"

    def scan_dynamic(self) -> Dict[str, Any]:
        """动态检测：编译检查（支持 JUnit / EvoSuite classpath）"""
        result = {
            "enabled": True,
            "compile_errors": [],
            "compile_success": False
        }
            # 添加新的动态检测
        try:
            from .dynamic_detector import JavaDynamicDetector
            detector = JavaDynamicDetector(self.files)
            dynamic_result = detector.detect_all()
            result["dynamic_detection"] = dynamic_result
        except Exception as e:
            result["dynamic_detection_error"] = str(e)
        tmp_dir = tempfile.mkdtemp(prefix="java_compile_")
        try:
            java_files = []
            for f in self.files:
                filename = f.get("file", "").replace("/", os.sep)
                if "InvalidImport" in filename:  # 🔥 跳过 EvoSuite 的无效导入文件
                    print(f"[DEBUG] 跳过无效文件: {filename}")
                    continue
                content = f.get("content", "")
                filepath = os.path.join(tmp_dir, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w", encoding="utf-8") as fp:
                    fp.write(content)
                java_files.append(filepath)

            # 🔍 自动收集项目中所有 JAR 包
            jar_paths = []
            search_dirs = [
                os.getcwd(),
                os.path.join(os.getcwd(), "lib"),
                os.path.join(os.getcwd(), "libs"),
                os.path.join(os.getcwd(), "dependencies"),
            ]
            for d in search_dirs:
                if os.path.exists(d):
                    for root, _, files in os.walk(d):
                        for fn in files:
                            if fn.endswith(".jar"):
                                jar_paths.append(os.path.join(root, fn))

            if not jar_paths:
                print("⚠️ 未发现任何 .jar 依赖，可能无法编译测试类（JUnit等）。")

            # 拼接 classpath（Windows 使用 ;，Linux/Mac 使用 :）
            sep = ";" if os.name == "nt" else ":"
            classpath = tmp_dir
            if jar_paths:
                classpath += sep + sep.join(jar_paths)

            print(f"[DEBUG] Java 编译 classpath:\n{classpath}")

            # 🔧 编译命令
            compile_cmd = [
                "javac",
                "-encoding", "UTF-8",
                "-d", tmp_dir,
                "-cp", classpath
            ] + java_files

            print(f"[DEBUG] 运行编译命令: {' '.join(compile_cmd[:10])} ... ({len(compile_cmd)} args)")

            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=90
            )

            if compile_result.returncode == 0:
                result["compile_success"] = True
                print("[DEBUG] ✅ 编译成功")
            else:
                stderr = compile_result.stderr.strip()
                print(f"[DEBUG] ❌ 编译失败输出:\n{stderr[:400]}")
                result["compile_success"] = False

                for line in stderr.split("\n"):
                    if ".java:" in line:
                        result["compile_errors"].append(line.strip())
                    elif "error:" in line.lower():
                        result["compile_errors"].append(line.strip())

        except subprocess.TimeoutExpired:
            result["compile_errors"].append("编译超时")
        except Exception as e:
            result["compile_errors"].append(f"编译失败: {e}")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        return result


    def scan_with_external_tools(self, *args, **kwargs):
        """统一调用外部工具（PMD/Checkstyle），修正返回结构"""
        try:
            # 处理参数
            if args and isinstance(args[0], dict):
                tool_config = args[0]
            else:
                tool_config = kwargs.get("tool_config")

            # 调用外部扫描
            findings = self.scan_external(tool_config)

            # ✅ 兼容性修正：始终返回 list[Finding]
            if isinstance(findings, dict):
                findings = findings.get("findings", []) or findings.get("defects", [])
            elif not isinstance(findings, list):
                print(f"[DEBUG] ⚠️ scan_external 返回未知类型: {type(findings)}")
                findings = []

            print(f"[DEBUG] ✅ scan_with_external_tools 发现 {len(findings)} 个问题")

            return findings  # <-- 注意，直接返回列表
        except Exception as e:
            import traceback
            print(f"⚠️ 外部工具扫描执行异常: {e}")
            traceback.print_exc()
            return []

    def scan(self) -> List[Finding]:
        """兼容 BaseScanner 接口，统一入口"""
        return self.scan_builtin()

    def check_compilation(self, *args, **kwargs):
        """兼容 ScannerAgent 调用旧接口的编译检查"""
        import inspect
        # print("\n[DEBUG][check_compilation] 被调用！")
        # print(f"[DEBUG] args: {args}")
        # print(f"[DEBUG] kwargs: {kwargs}")

        # stack = inspect.stack()
        # print("[DEBUG] 调用来源（从近到远）:")
        # for frame in stack[1:5]:
        #     print(f"   - {frame.function}() in {os.path.basename(frame.filename)}:{frame.lineno}")

        try:
            result = self.scan_dynamic()
            print(f"[DEBUG] scan_dynamic 返回 keys: {list(result.keys())}")
            return {"compile_result": result, "success": True}
        except Exception as e:
            import traceback
            print(f"⚠️ 编译检查异常: {e}")
            traceback.print_exc()
            return {"compile_result": {}, "success": False, "error": str(e)}





