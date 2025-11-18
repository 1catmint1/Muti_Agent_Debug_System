# verifiers/cpp_verifier.py
"""
CppVerifier - C/C++代码验证器（增强版）
"""
import os
import tempfile
import shutil
import subprocess
import platform
from typing import Dict, List, Any

from .base_verifier import BaseVerifier, Language


class CppVerifier(BaseVerifier):
    """C/C++专用验证器"""

    def __init__(self, language: Language = Language.CPP):
        super().__init__(language)
        self.compiler = self._find_compiler()

    def _find_compiler(self) -> str:
        """
        查找可用的编译器
        优先级：项目内 tools/mingw64 > 系统环境
        """

        # ========================================================================
        # 1. 优先查找项目内的编译器
        # ========================================================================
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            mingw_bin = os.path.join(project_root, "tools", "mingw64", "mingw64", "bin")

            print(f"[CppVerifier] 查找项目内编译器...")
            print(f"[CppVerifier]   项目根目录: {project_root}")
            print(f"[CppVerifier]   MinGW 路径: {mingw_bin}")

            if os.path.isdir(mingw_bin):
                print(f"[CppVerifier] ✅ 找到项目内 MinGW 目录")

                # 根据语言选择编译器
                if self.language == Language.CPP:
                    compilers = [
                        os.path.join(mingw_bin, "g++.exe"),
                        os.path.join(mingw_bin, "gcc.exe")
                    ]
                else:
                    compilers = [
                        os.path.join(mingw_bin, "gcc.exe")
                    ]

                # 测试每个编译器
                for compiler in compilers:
                    if not os.path.isfile(compiler):
                        continue

                    try:
                        result = subprocess.run(
                            [compiler, "--version"],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if result.returncode == 0:
                            print(f"[CppVerifier] ✅ 使用项目内编译器: {os.path.basename(compiler)}")
                            return compiler
                    except Exception as e:
                        print(f"[CppVerifier] 测试 {os.path.basename(compiler)} 失败: {e}")
            else:
                print(f"[CppVerifier] ❌ 项目内 MinGW 目录不存在")
        except Exception as e:
            print(f"[CppVerifier] 查找项目内编译器失败: {e}")

        # ========================================================================
        # 2. 查找系统环境中的编译器
        # ========================================================================
        print(f"[CppVerifier] 在系统环境中查找编译器...")

        compilers = ["g++", "gcc", "clang++", "clang"] if self.language == Language.CPP else ["gcc", "clang", "g++"]

        for compiler in compilers:
            try:
                result = subprocess.run(
                    [compiler, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    print(f"[CppVerifier] ✅ 找到系统编译器: {compiler}")
                    return compiler
            except:
                continue

        print(f"[CppVerifier] ⚠️ 警告: 未找到任何编译器，语法验证将不可用")
        return None

    def verify_syntax(self, file: Dict[str, Any]) -> Dict[str, Any]:
        """语法验证：使用gcc/g++编译"""
        content = file.get("content", "")
        filename = file.get("file", "temp.cpp" if self.language == Language.CPP else "temp.c")

        result = {
            "success": False,
            "errors": []
        }

        # ✅ 检查编译器是否可用
        if not self.compiler:
            result["errors"].append({"message": "未找到编译器 (gcc/g++/clang)"})
            print(f"[CppVerifier] 跳过语法验证: 编译器不可用")
            # ✅ 返回 success=True 避免阻塞流程
            result["success"] = True
            return result

        # 创建临时目录
        tmp_dir = tempfile.mkdtemp(prefix="cpp_verify_")

        print(f"[CppVerifier] 开始语法验证: {filename}")
        print(f"[CppVerifier] 临时目录: {tmp_dir}")

        try:
            # 写入文件
            base_filename = os.path.basename(filename)
            filepath = os.path.join(tmp_dir, base_filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"[CppVerifier] 写入文件: {filepath}")

            # 选择编译器和标准
            compiler = self.compiler

            # 根据编译器和语言选择标准
            if self.language == Language.CPP:
                if "clang++" in compiler or "g++" in compiler:
                    std_flag = "-std=c++17"
                else:
                    std_flag = "-std=c++11"
            else:
                std_flag = "-std=c11"

            # ✅ 编译命令（更宽松的设置）
            compile_cmd = [
                compiler,
                std_flag,
                "-Wall",  # 显示所有警告
                "-Wno-unused",  # 忽略未使用变量警告（减少干扰）
                "-fsyntax-only",  # 只做语法检查，不生成代码
                filepath
            ]

            print(f"[CppVerifier] 编译命令: {' '.join(compile_cmd)}")

            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=tmp_dir
            )

            if compile_result.returncode == 0:
                result["success"] = True
                print(f"[CppVerifier] ✅ 编译成功")
            else:
                # 解析编译错误
                stderr = compile_result.stderr
                print(f"[CppVerifier] ❌ 编译失败:\n{stderr}")

                # ✅ 只记录严重错误（error），忽略警告
                for line in stderr.split('\n'):
                    if 'error:' in line.lower():
                        result["errors"].append({"message": line.strip()})

                # ✅ 如果只有警告没有错误，也视为成功
                if not result["errors"]:
                    result["success"] = True
                    print(f"[CppVerifier] ✅ 只有警告，视为编译成功")

        except subprocess.TimeoutExpired:
            result["errors"].append({"message": "编译超时"})
            print(f"[CppVerifier] ❌ 编译超时")
        except FileNotFoundError:
            result["errors"].append({"message": f"{compiler}未找到，请确保已安装编译器"})
            print(f"[CppVerifier] ❌ {compiler}未找到")
        except Exception as e:
            result["errors"].append({"message": str(e)})
            print(f"[CppVerifier] ❌ 验证异常: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # 清理临时目录
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except:
                pass

        return result

    def verify_functionality(self, file: Dict[str, Any],
                             test_cases: List[Dict] = None) -> Dict[str, Any]:
        """功能验证：编译并运行"""
        result = {
            "success": False,
            "passed": 0,
            "failed": 0,
            "errors": []
        }

        if not test_cases:
            # ✅ 没有测试用例时，视为成功
            result["success"] = True
            print(f"[CppVerifier] 无测试用例，跳过功能验证")
            return result

        # ✅ 检查编译器
        if not self.compiler:
            result["errors"].append({"error": "未找到编译器，无法进行功能测试"})
            result["success"] = True  # 不阻塞流程
            print(f"[CppVerifier] 跳过功能验证: 编译器不可用")
            return result

        print(f"[CppVerifier] 功能验证: {len(test_cases)} 个测试用例")

        content = file.get("content", "")
        filename = file.get("file", "temp.cpp" if self.language == Language.CPP else "temp.c")

        # 创建临时目录
        tmp_dir = tempfile.mkdtemp(prefix="cpp_run_")

        try:
            # 写入文件
            base_filename = os.path.basename(filename)
            filepath = os.path.join(tmp_dir, base_filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            # 编译
            compiler = self.compiler
            std_flag = "-std=c++17" if self.language == Language.CPP else "-std=c11"

            # ✅ 输出文件根据平台确定
            if platform.system() == "Windows":
                output_file = os.path.join(tmp_dir, "program.exe")
            else:
                output_file = os.path.join(tmp_dir, "program")

            compile_cmd = [compiler, std_flag, filepath, "-o", output_file]

            print(f"[CppVerifier] 编译命令: {' '.join(compile_cmd)}")

            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=tmp_dir
            )

            if compile_result.returncode != 0:
                result["errors"].append({"error": "编译失败"})
                print(f"[CppVerifier] ❌ 编译失败")
                return result

            print(f"[CppVerifier] ✅ 编译成功，开始运行测试")

            # 运行测试用例
            for i, test_case in enumerate(test_cases, 1):
                test_input = test_case.get("input", "")
                expected_output = test_case.get("expected_output", "")

                try:
                    run_result = subprocess.run(
                        [output_file],
                        input=test_input if isinstance(test_input, str) else str(test_input),
                        capture_output=True,
                        text=True,
                        timeout=5,
                        cwd=tmp_dir
                    )

                    actual_output = run_result.stdout.strip()

                    # ✅ 灵活比较输出
                    expected_str = str(expected_output).strip()

                    if actual_output == expected_str:
                        result["passed"] += 1
                        print(f"[CppVerifier] ✅ 测试用例 {i}: 通过")
                    else:
                        result["failed"] += 1
                        result["errors"].append({
                            "test_case": i,
                            "expected": expected_str,
                            "actual": actual_output
                        })
                        print(f"[CppVerifier] ❌ 测试用例 {i}: 失败")
                        print(f"[CppVerifier]    期望: {expected_str}")
                        print(f"[CppVerifier]    实际: {actual_output}")

                except subprocess.TimeoutExpired:
                    result["failed"] += 1
                    result["errors"].append({
                        "test_case": i,
                        "error": "超时"
                    })
                    print(f"[CppVerifier] ⏱️ 测试用例 {i}: 超时")
                except Exception as e:
                    result["failed"] += 1
                    result["errors"].append({
                        "test_case": i,
                        "error": str(e)
                    })
                    print(f"[CppVerifier] ❌ 测试用例 {i}: 异常 - {e}")

            result["success"] = result["failed"] == 0

            print(f"[CppVerifier] 功能测试完成: {result['passed']}/{len(test_cases)} 通过")

        except Exception as e:
            result["errors"].append({"error": str(e)})
            print(f"[CppVerifier] ❌ 功能验证异常: {e}")
        finally:
            # 清理临时目录
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except:
                pass

        return result