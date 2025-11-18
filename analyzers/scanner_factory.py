"""
ScannerFactory - 根据语言创建对应的扫描器
"""
import sys
import os
from typing import List, Dict, Any

# 添加路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.language_detector import Language
from .base_scanner import BaseScanner
from .defect_scanner import DefectScanner  # Python 扫描器
from .java_scanner import JavaScanner
from .cpp_scanner import CppScanner


class DefectScannerAdapter:
    """
    适配器：将 DefectScanner 对接多-Agent 扫描接口

    对 ScannerAgent 而言：
    - scan()                -> 返回内置静态缺陷列表(list[dict])
    - scan_with_external_tools(files) -> 返回外部工具缺陷列表(list[dict])
    - check_compilation(files)        -> 返回 {"compile_result": {...}, "success": bool}
    """

    def __init__(self, files: List[Dict[str, Any]]):
        self.scanner = DefectScanner(files)
        self.files = files

    def scan(self) -> List[Dict[str, Any]]:
        """
        执行内置规则扫描（不启用外部工具/动态），返回缺陷列表。
        ScannerAgent 会把返回值当作 builtin_defects。
        """
        result = self.scanner.scan(
            enable_external=False,
            enable_dynamic=False
        )
        static_builtin = result.get("static_builtin", [])

        # DefectScanner.scan 返回的 static_builtin 已经是 asdict(Finding) 的列表
        if isinstance(static_builtin, list):
            return static_builtin

        return []

    def scan_with_external_tools(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        使用外部工具扫描，返回缺陷列表。
        ScannerAgent 会把返回值当作 external_defects。
        """
        result = self.scanner.scan(
            enable_external=True,
            enable_dynamic=False
        )

        external_defects: List[Dict[str, Any]] = []
        external_data = result.get("external", {}) or {}

        # 遍历所有外部工具的结果
        for tool_name, tool_data in external_data.items():
            if isinstance(tool_data, dict):
                findings = tool_data.get("findings", [])
                if isinstance(findings, list):
                    for it in findings:
                        if isinstance(it, dict):
                            d = it.copy()
                            d.setdefault("tool", tool_name)
                            external_defects.append(d)
            elif isinstance(tool_data, list):
                # 直接是列表的，统一视为缺陷
                for it in tool_data:
                    if isinstance(it, dict):
                        external_defects.append(it)

        return external_defects

    def check_compilation(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        执行简单编译检查（py_compile），返回结构供 ScannerAgent 包裹：

        返回:
            {
                "compile_result": { "py_compile": [...], "pytest": {...}, ... },
                "success": bool
            }
        """
        result = self.scanner.scan(
            enable_external=False,
            enable_dynamic=True
        )

        dynamic = result.get("dynamic", {})
        compile_errors = dynamic.get("py_compile", [])

        return {
            "compile_result": {
                "py_compile": compile_errors,
                **{k: v for k, v in dynamic.items() if k != "py_compile"}
            },
            "success": len(compile_errors) == 0
        }


class ScannerFactory:
    """扫描器工厂"""

    @staticmethod
    def create_scanner(files: list, language: Language):
        """
        根据语言创建对应的扫描器

        Args:
            files: 文件列表
            language: 目标语言

        Returns:
            对应语言的扫描器实例
        """
        if language == Language.PYTHON:
            # ✅ Python 使用 DefectScannerAdapter，接口风格与 ScannerAgent 预期一致
            return DefectScannerAdapter(files)

        elif language == Language.JAVA:
            return JavaScanner(files)

        elif language == Language.CPP or language == Language.C:
            return CppScanner(files, language)

        else:
            raise ValueError(f"不支持的语言: {language}")

    @staticmethod
    def get_supported_languages():
        """获取支持的语言列表"""
        return [Language.PYTHON, Language.JAVA, Language.C, Language.CPP]