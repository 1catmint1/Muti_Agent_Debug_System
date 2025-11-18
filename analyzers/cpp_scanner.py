# scanners/cpp_scanner.py
"""
CppScanner - C/C++代码扫描器（使用项目内嵌的 cppcheck）
"""
import subprocess
import os
import platform
import re
from typing import Dict, List, Any

from .base_scanner import BaseScanner, Language
from utils.common import Finding


class CppScanner(BaseScanner):
    """C/C++专用扫描器（基于cppcheck）"""

    def __init__(self, files: List[Dict[str, Any]], language: Language = Language.CPP):
        super().__init__(files, language)
        self.tool_name = "cppcheck"

        # ✅ 自动查找并使用 cppcheck
        self.cppcheck_path = self._find_cppcheck()

        if not self.cppcheck_path:
            print(f"[CppScanner] ⚠️ 警告: cppcheck 未找到")
            print(f"[CppScanner] 将使用内置规则扫描")
        else:
            print(f"[CppScanner] ✅ 使用 cppcheck: {self.cppcheck_path}")
            self._check_tool_version()

    def _find_cppcheck(self) -> str:
        """
        查找 cppcheck 路径
        优先级：项目内 tools/cppcheck > 系统环境
        """
        # 1. 项目内工具路径（递归查找）
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 根据操作系统确定可执行文件名
        exe_name = "cppcheck.exe" if platform.system() == "Windows" else "cppcheck"

        # ✅ 递归查找 tools/cppcheck 下的所有可能路径
        tools_cppcheck_dir = os.path.join(project_root, "tools", "cppcheck")

        if os.path.isdir(tools_cppcheck_dir):
            print(f"[CppScanner] 在 {tools_cppcheck_dir} 中查找 cppcheck...")

            # 递归搜索
            for root, dirs, files in os.walk(tools_cppcheck_dir):
                if exe_name in files:
                    path = os.path.join(root, exe_name)
                    # 确保可执行权限（Linux/macOS）
                    if platform.system() != "Windows":
                        try:
                            os.chmod(path, 0o755)
                        except:
                            pass
                    print(f"[CppScanner] 找到项目内工具: {path}")
                    return path

        # 2. 其他可能的项目内路径
        other_paths = [
            os.path.join(project_root, "tools", "cppcheck", exe_name),
            os.path.join(project_root, "bin", exe_name),
        ]

        for path in other_paths:
            if os.path.isfile(path):
                if platform.system() != "Windows":
                    try:
                        os.chmod(path, 0o755)
                    except:
                        pass
                print(f"[CppScanner] 找到项目内工具: {path}")
                return path

        # 3. 系统环境中的 cppcheck
        try:
            result = subprocess.run(
                [exe_name, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"[CppScanner] 找到系统工具: {exe_name}")
                return exe_name
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        # 4. 尝试通过 which/where 查找
        try:
            find_cmd = "where" if platform.system() == "Windows" else "which"
            result = subprocess.run(
                [find_cmd, "cppcheck"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                path = result.stdout.strip().split('\n')[0]
                if os.path.isfile(path):
                    print(f"[CppScanner] 通过 {find_cmd} 找到: {path}")
                    return path
        except:
            pass

        print(f"[CppScanner] 未找到 cppcheck，搜索路径:")
        print(f"[CppScanner]   - {tools_cppcheck_dir}")
        print(f"[CppScanner]   - 系统环境变量")

        return None

    def _check_tool_version(self) -> bool:
        """检查 cppcheck 版本"""
        if not self.cppcheck_path:
            return False

        try:
            result = subprocess.run(
                [self.cppcheck_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"[CppScanner] 检测到 {version}")
                return True
        except Exception as e:
            print(f"[CppScanner] 版本检查失败: {e}")
        return False

    # ========================================================================
    # ✅ 实现 BaseScanner 要求的抽象方法（返回 List[Finding]）
    # ========================================================================

    def scan_builtin(self) -> List[Finding]:
        """使用内置规则扫描（实现抽象方法）"""
        print(f"[CppScanner] 使用内置规则扫描 {len(self.files)} 个文件...")

        findings = []

        for file_info in self.files:
            file_path = file_info.get("file", "")
            content = file_info.get("content", "")

            print(f"[CppScanner] 扫描文件: {file_path}")

            file_issues = self._scan_with_builtin_rules(file_path, content)

            for issue in file_issues:
                finding = Finding(
                    file=file_path,
                    line=issue.get("line", 0),
                    column=issue.get("column", 0),
                    severity=issue.get("severity", "MEDIUM"),
                    message=issue.get("message", ""),
                    rule_id=issue.get("rule_id", ""),
                    tool=issue.get("tool", "builtin")
                )
                findings.append(finding)

        print(f"[CppScanner] 内置规则扫描完成: 发现 {len(findings)} 个问题")

        return findings

    def scan_external(self, tool_config: Dict[str, bool] = None) -> List[Finding]:
        """使用外部工具扫描（实现抽象方法）"""
        print(f"[CppScanner] 使用 cppcheck 扫描 {len(self.files)} 个文件...")

        findings = []

        if not self.cppcheck_path:
            print(f"[CppScanner] cppcheck 不可用，跳过外部扫描")
            return findings

        for file_info in self.files:
            file_path = file_info.get("file", "")
            content = file_info.get("content", "")

            print(f"[CppScanner] 扫描文件: {file_path}")

            file_issues = self._scan_with_cppcheck(file_path, content)

            for issue in file_issues:
                finding = Finding(
                    file=file_path,
                    line=issue.get("line", 0),
                    column=issue.get("column", 0),
                    severity=issue.get("severity", "MEDIUM"),
                    message=issue.get("message", ""),
                    rule_id=issue.get("rule_id", ""),
                    tool=issue.get("tool", "cppcheck")
                )
                findings.append(finding)

        print(f"[CppScanner] cppcheck 扫描完成: 发现 {len(findings)} 个问题")

        return findings

    # ========================================================================
    # ========================================================================
    # ✅ 添加 ScannerAgent 需要的方法（修复参数）
    # ========================================================================

    def scan_with_external_tools(self, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """外部工具扫描（ScannerAgent 调用）"""
        print(f"[CppScanner] scan_with_external_tools 被调用")

        if not self.cppcheck_path:
            print(f"[CppScanner] cppcheck 不可用，返回空结果")
            return {
                "tool": self.tool_name,
                "language": self.language.value,
                "files_scanned": 0,
                "issues_found": 0,
                "defects": []  # ✅ 改为 "defects" 以匹配 scanner_agent.py
            }

        # 调用 scan_external 并正确返回结果
        findings = self.scan_external()

        print(f"[CppScanner] scan_external 返回了 {len(findings)} 个问题")

        # 转换为字典格式
        defects_list = [f.to_dict() for f in findings]

        result = {
            "tool": self.tool_name,
            "language": self.language.value,
            "files_scanned": len(self.files),
            "issues_found": len(findings),
            "defects": defects_list  # ✅ 改为 "defects" 以匹配 scanner_agent.py
        }

        print(f"[CppScanner] 返回结果: files_scanned={result['files_scanned']}, issues_found={result['issues_found']}")

        return result

    def check_compilation(self, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """编译检查（ScannerAgent 调用）"""
        print(f"[CppScanner] check_compilation 被调用")

        if config:
            print(f"[CppScanner] 配置: {config}")

        # 查找编译器
        compiler = self._find_compiler()

        if not compiler:
            print(f"[CppScanner] 未找到编译器，跳过编译检查")
            return {
                "enabled": False,
                "message": "未找到编译器"
            }

        results = {
            "enabled": True,
            "compiler": compiler,
            "files_checked": 0,
            "success": 0,
            "failed": 0,
            "errors": []
        }

        for file_info in self.files:
            file_path = file_info.get("file", "")
            content = file_info.get("content", "")

            print(f"[CppScanner] 编译检查: {file_path}")

            compile_result = self._check_file_compilation(compiler, file_path, content)

            results["files_checked"] += 1

            if compile_result["success"]:
                results["success"] += 1
            else:
                results["failed"] += 1
                results["errors"].extend(compile_result.get("errors", []))

        print(f"[CppScanner] 编译检查完成: {results['success']}/{results['files_checked']} 通过")

        return results

    def _find_compiler(self) -> str:
        """
        查找可用的编译器
        优先级：项目内 tools/mingw64 > 系统环境
        """

        # ========================================================================
        # 1. 优先查找项目内的编译器
        # ========================================================================
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mingw_bin = os.path.join(project_root, "tools", "mingw64","mingw64", "bin")

        print(f"[CppScanner] 查找项目内编译器...")
        print(f"[CppScanner]   项目根目录: {project_root}")
        print(f"[CppScanner]   MinGW 路径: {mingw_bin}")

        if os.path.isdir(mingw_bin):
            print(f"[CppScanner] ✅ 找到项目内 MinGW 目录")

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
                print(f"[CppScanner]   测试: {compiler}")

                if not os.path.isfile(compiler):
                    print(f"[CppScanner]     ❌ 文件不存在")
                    continue

                try:
                    result = subprocess.run(
                        [compiler, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        print(f"[CppScanner]     ✅ 可用！使用: {os.path.basename(compiler)}")
                        return compiler
                    else:
                        print(f"[CppScanner]     ❌ 返回码: {result.returncode}")
                except Exception as e:
                    print(f"[CppScanner]     ❌ 测试失败: {e}")
        else:
            print(f"[CppScanner] ❌ 项目内 MinGW 目录不存在")

        # ========================================================================
        # 2. 查找系统环境中的编译器
        # ========================================================================
        print(f"[CppScanner] 在系统环境中查找编译器...")

        if self.language == Language.CPP:
            compilers = ["g++", "gcc", "clang++", "clang"]
        else:
            compilers = ["gcc", "clang"]

        for compiler in compilers:
            try:
                result = subprocess.run(
                    [compiler, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    print(f"[CppScanner] ✅ 找到系统编译器: {compiler}")
                    return compiler
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"[CppScanner] 测试 {compiler} 失败: {e}")
                continue

        print(f"[CppScanner] ❌ 未找到任何编译器")
        print(f"[CppScanner] 提示: 请确保 MinGW 已安装到 tools/mingw64/")
        return None

    def _check_file_compilation(self, compiler: str, file_path: str, content: str) -> Dict[str, Any]:
        """检查单个文件是否能编译"""
        import tempfile

        result = {
            "success": False,
            "errors": []
        }

        try:
            # 创建临时文件
            suffix = '.cpp' if self.language == Language.CPP else '.c'
            with tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix=suffix,
                    delete=False,
                    encoding='utf-8'
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name

            try:
                # 编译
                std_flag = "-std=c++17" if self.language == Language.CPP else "-std=c11"

                cmd = [
                    compiler,
                    std_flag,
                    "-Wall",
                    "-Wno-unused",
                    "-fsyntax-only",  # 只做语法检查
                    tmp_path
                ]

                compile_result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if compile_result.returncode == 0:
                    result["success"] = True
                else:
                    # 只记录错误，不记录警告
                    for line in compile_result.stderr.split('\n'):
                        if 'error:' in line.lower():
                            result["errors"].append({
                                "file": file_path,
                                "message": line.strip()
                            })

                    # 如果没有错误只有警告，也算成功
                    if not result["errors"]:
                        result["success"] = True

            finally:
                try:
                    os.unlink(tmp_path)
                except:
                    pass

        except Exception as e:
            result["errors"].append({
                "file": file_path,
                "message": f"编译检查异常: {str(e)}"
            })

        return result

    # ========================================================================
    # 内部实现方法
    # ========================================================================

    def _scan_with_cppcheck(self, file_path: str, content: str) -> List[Dict]:
        """使用 cppcheck 扫描"""
        issues = []

        try:
            import tempfile

            # 创建临时文件
            suffix = '.cpp' if self.language == Language.CPP else '.c'
            with tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix=suffix,
                    delete=False,
                    encoding='utf-8'
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name

            try:
                # 运行 cppcheck
                cmd = [
                    self.cppcheck_path,
                    "--enable=all",
                    "--inline-suppr",
                    "--template=gcc",
                    "--quiet",
                    "--force",
                    tmp_path
                ]

                print(f"[CppScanner] 执行: {os.path.basename(cmd[0])} {' '.join(cmd[1:])}")

                cwd = os.path.dirname(self.cppcheck_path) if os.path.isabs(self.cppcheck_path) else None

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=cwd
                )

                output = result.stderr

                print(f"[CppScanner] 输出长度: {len(output)} 字符")

                if output:
                    issues = self._parse_cppcheck_output(output, file_path)
                else:
                    print(f"[CppScanner] cppcheck 未返回问题")

            finally:
                try:
                    os.unlink(tmp_path)
                except:
                    pass

        except subprocess.TimeoutExpired:
            print(f"[CppScanner] cppcheck 超时")
        except FileNotFoundError:
            print(f"[CppScanner] cppcheck 未找到: {self.cppcheck_path}")
        except Exception as e:
            print(f"[CppScanner] cppcheck 执行失败: {e}")
            import traceback
            traceback.print_exc()

        return issues

    def _parse_cppcheck_output(self, output: str, file_path: str) -> List[Dict]:
        """解析 cppcheck 输出"""
        issues = []

        pattern = r'^(.+?):(\d+)(?::(\d+))?: (\w+): (.+?) \[(\w+)\]'

        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue

            match = re.match(pattern, line)
            if match:
                file, line_num, column, severity, message, rule_id = match.groups()

                issues.append({
                    "line": int(line_num),
                    "column": int(column) if column else 0,
                    "severity": self._map_severity(severity),
                    "message": message.strip(),
                    "rule_id": rule_id,
                    "tool": "cppcheck"
                })

        return issues

    def _map_severity(self, cppcheck_severity: str) -> str:
        """映射 cppcheck 严重程度到标准级别"""
        mapping = {
            "error": "HIGH",
            "warning": "MEDIUM",
            "style": "LOW",
            "performance": "MEDIUM",
            "portability": "LOW",
            "information": "INFO"
        }
        return mapping.get(cppcheck_severity.lower(), "MEDIUM")

    def _scan_with_builtin_rules(self, file_path: str, content: str) -> List[Dict]:
        """使用内置规则扫描（备用方案）"""
        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            # 规则1: 检测 gets()
            if re.search(r'\bgets\s*\(', line):
                issues.append({
                    "line": line_num,
                    "column": 0,
                    "severity": "HIGH",
                    "message": "使用不安全的 gets() 函数，应使用 fgets()",
                    "rule_id": "CPP001",
                    "tool": "builtin"
                })

            # 规则2: 检测 strcpy()
            if re.search(r'\bstrcpy\s*\(', line):
                issues.append({
                    "line": line_num,
                    "column": 0,
                    "severity": "MEDIUM",
                    "message": "使用不安全的 strcpy() 函数，应使用 strncpy()",
                    "rule_id": "CPP002",
                    "tool": "builtin"
                })

            # 规则3: 检测 sprintf()
            if re.search(r'\bsprintf\s*\(', line):
                issues.append({
                    "line": line_num,
                    "column": 0,
                    "severity": "MEDIUM",
                    "message": "使用不安全的 sprintf() 函数，应使用 snprintf()",
                    "rule_id": "CPP003",
                    "tool": "builtin"
                })

            # 规则4: 检测 malloc 后未检查 NULL
            if re.search(r'\w+\s*=\s*(malloc|calloc|realloc)\s*\(', line):
                has_null_check = False
                for check_line in lines[line_num:min(line_num + 5, len(lines))]:
                    if 'NULL' in check_line or 'nullptr' in check_line:
                        has_null_check = True
                        break

                if not has_null_check:
                    issues.append({
                        "line": line_num,
                        "column": 0,
                        "severity": "HIGH",
                        "message": "内存分配后未检查 NULL 指针",
                        "rule_id": "CPP004",
                        "tool": "builtin"
                    })

            # 规则5: 检测数组越界风险
            if re.search(r'\[\s*\w+\s*\]', line) and 'sizeof' not in line:
                if re.search(r'for\s*\(.*<.*\)', line):
                    issues.append({
                        "line": line_num,
                        "column": 0,
                        "severity": "MEDIUM",
                        "message": "可能存在数组越界风险，建议检查边界条件",
                        "rule_id": "CPP005",
                        "tool": "builtin"
                    })

            # 规则6: 检测未初始化的变量
            if re.search(r'^\s*(int|char|float|double|long)\s+\w+\s*;', line):
                issues.append({
                    "line": line_num,
                    "column": 0,
                    "severity": "MEDIUM",
                    "message": "变量声明时未初始化",
                    "rule_id": "CPP006",
                    "tool": "builtin"
                })

        return issues