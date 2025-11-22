# analyzers/dynamic_detector.py
# -*- coding: utf-8 -*-
"""
DynamicDetector - 动态检测模块
支持运行时检测以下问题：
1. 用户输入与外部数据交互点
2. 资源管理与状态依赖
3. 并发与异步操作
4. 边界条件与异常处理
5. 环境依赖与配置
6. 动态代码执行
"""

import os
import re
import ast
import json
import tempfile
import subprocess
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field


@dataclass
class DynamicFinding:
    """动态检测发现的问题"""
    file: str
    line: int
    col: int = 0
    category: str = ""  # user_input, resource_management, concurrency, etc.
    severity: str = "MEDIUM"  # HIGH / MEDIUM / LOW
    rule_id: str = ""
    message: str = ""
    snippet: str = ""
    suggestion: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file,
            "line": self.line,
            "col": self.col,
            "category": self.category,
            "severity": self.severity,
            "rule_id": self.rule_id,
            "message": self.message,
            "snippet": self.snippet,
            "suggestion": self.suggestion
        }


class DynamicDetector:
    """动态检测器基类"""
    
    def __init__(self, files: List[Dict[str, Any]]):
        """
        Args:
            files: [{"file": "xxx", "content": "...", ...}, ...]
        """
        self.files = files
        self.findings: List[DynamicFinding] = []
    
    def detect_all(self) -> Dict[str, Any]:
        """执行所有动态检测"""
        result = {
            "enabled": True,
            "categories": {
                "user_input": [],
                "resource_management": [],
                "concurrency": [],
                "boundary_conditions": [],
                "environment_config": [],
                "dynamic_execution": []
            },
            "summary": {
                "total": 0,
                "by_category": {},
                "by_severity": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            }
        }
        
        # 检测各个类别
        self.detect_user_input()
        self.detect_resource_management()
        self.detect_concurrency()
        self.detect_boundary_conditions()
        self.detect_environment_config()
        self.detect_dynamic_execution()
        
        # 汇总结果
        for finding in self.findings:
            category = finding.category or "other"
            if category not in result["categories"]:
                result["categories"][category] = []
            result["categories"][category].append(finding.to_dict())
            
            # 统计
            result["summary"]["by_severity"][finding.severity] = \
                result["summary"]["by_severity"].get(finding.severity, 0) + 1
            result["summary"]["by_category"][category] = \
                result["summary"]["by_category"].get(category, 0) + 1
        
        result["summary"]["total"] = len(self.findings)
        
        return result
    
    def detect_user_input(self):
        """检测用户输入与外部数据交互点"""
        pass  # 由子类实现
    
    def detect_resource_management(self):
        """检测资源管理与状态依赖"""
        pass  # 由子类实现
    
    def detect_concurrency(self):
        """检测并发与异步操作"""
        pass  # 由子类实现
    
    def detect_boundary_conditions(self):
        """检测边界条件与异常处理"""
        pass  # 由子类实现
    
    def detect_environment_config(self):
        """检测环境依赖与配置"""
        pass  # 由子类实现
    
    def detect_dynamic_execution(self):
        """检测动态代码执行"""
        pass  # 由子类实现


class PythonDynamicDetector(DynamicDetector):
    """Python 动态检测器"""
    
    def __init__(self, files: List[Dict[str, Any]]):
        super().__init__(files)
        self.file_map: Dict[str, str] = {}
        for f in files:
            name = f.get("file") or f.get("path") or ""
            if name.endswith('.py'):
                self.file_map[name] = f.get("content", "")
    
    def detect_user_input(self):
        """检测用户输入与外部数据交互点"""
        for filename, content in self.file_map.items():
            try:
                tree = ast.parse(content, filename=filename)
                visitor = UserInputVisitor(content, filename)
                visitor.visit(tree)
                self.findings.extend(visitor.findings)
            except SyntaxError:
                pass
    
    def detect_resource_management(self):
        """检测资源管理与状态依赖"""
        for filename, content in self.file_map.items():
            try:
                tree = ast.parse(content, filename=filename)
                visitor = ResourceManagementVisitor(content, filename)
                visitor.visit(tree)
                self.findings.extend(visitor.findings)
            except SyntaxError:
                pass
    
    def detect_concurrency(self):
        """检测并发与异步操作"""
        for filename, content in self.file_map.items():
            try:
                tree = ast.parse(content, filename=filename)
                visitor = ConcurrencyVisitor(content, filename)
                visitor.visit(tree)
                self.findings.extend(visitor.findings)
            except SyntaxError:
                pass
    
    def detect_boundary_conditions(self):
        """检测边界条件与异常处理"""
        for filename, content in self.file_map.items():
            try:
                tree = ast.parse(content, filename=filename)
                visitor = BoundaryConditionsVisitor(content, filename)
                visitor.visit(tree)
                self.findings.extend(visitor.findings)
            except SyntaxError:
                pass
    
    def detect_environment_config(self):
        """检测环境依赖与配置"""
        for filename, content in self.file_map.items():
            try:
                tree = ast.parse(content, filename=filename)
                visitor = EnvironmentConfigVisitor(content, filename)
                visitor.visit(tree)
                self.findings.extend(visitor.findings)
            except SyntaxError:
                pass
    
    def detect_dynamic_execution(self):
        """检测动态代码执行"""
        for filename, content in self.file_map.items():
            try:
                tree = ast.parse(content, filename=filename)
                visitor = DynamicExecutionVisitor(content, filename)
                visitor.visit(tree)
                self.findings.extend(visitor.findings)
            except SyntaxError:
                pass


class UserInputVisitor(ast.NodeVisitor):
    """用户输入与外部数据交互检测"""
    
    def __init__(self, code: str, filename: str):
        self.code = code
        self.filename = filename
        self.findings: List[DynamicFinding] = []
        self._lines = code.splitlines()
    
    def _add(self, node: ast.AST, rule_id: str, message: str, severity: str = "MEDIUM", suggestion: str = ""):
        line = getattr(node, "lineno", 1) or 1
        col = getattr(node, "col_offset", 0) or 0
        snippet = self._lines[line - 1][:200] if 1 <= line <= len(self._lines) else ""
        self.findings.append(DynamicFinding(
            file=self.filename,
            line=line,
            col=col,
            category="user_input",
            severity=severity,
            rule_id=rule_id,
            message=message,
            snippet=snippet,
            suggestion=suggestion
        ))
    
    def visit_Call(self, node: ast.Call):
        # HTTP 请求参数
        if isinstance(node.func, ast.Attribute):
            # requests.get/post
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id in ('requests', 'urllib', 'http') and
                node.func.attr in ('get', 'post', 'put', 'delete', 'request')):
                
                # 检查是否有参数验证
                self._add(node, "DYN-INPUT-001", 
                         f"HTTP 请求 {node.func.attr}() 可能包含未验证的参数",
                         "MEDIUM",
                         "建议验证请求参数，使用参数化查询，并添加输入清理")
            
            # Flask/Django request.args, request.form
            elif (isinstance(node.func.value, ast.Name) and 
                  node.func.value.id == 'request' and
                  node.func.attr in ('args', 'form', 'json', 'data', 'files')):
                
                self._add(node, "DYN-INPUT-002",
                         f"Web 框架获取用户输入 request.{node.func.attr}，需要验证和清理",
                         "HIGH",
                         "使用白名单验证，清理特殊字符，防止注入攻击")
        
        # JSON 解析
        if isinstance(node.func, ast.Attribute) and node.func.attr in ('loads', 'load'):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 'json':
                self._add(node, "DYN-INPUT-003",
                         "JSON 反序列化可能处理不可信数据",
                         "MEDIUM",
                         "验证 JSON 结构，使用 schema 验证，限制嵌套深度")
        
        # XML 解析
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ('parse', 'fromstring', 'XML'):
                attr_name = getattr(node.func.value, 'id', '')
                if 'xml' in attr_name.lower() or 'etree' in attr_name.lower():
                    self._add(node, "DYN-INPUT-004",
                             "XML 解析可能受到 XXE 攻击",
                             "HIGH",
                             "禁用外部实体，使用 defusedxml 库")
        
        # Cookie 操作
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id in ('cookies', 'cookie') and
                node.func.attr in ('get', 'set')):
                self._add(node, "DYN-INPUT-005",
                         "Cookie 操作需要验证和加密",
                         "MEDIUM",
                         "验证 Cookie 值，使用 HttpOnly 和 Secure 标志")
        
        self.generic_visit(node)


class ResourceManagementVisitor(ast.NodeVisitor):
    """资源管理与状态依赖检测"""
    
    def __init__(self, code: str, filename: str):
        self.code = code
        self.filename = filename
        self.findings: List[DynamicFinding] = []
        self._lines = code.splitlines()
        self.open_files: Set[str] = set()
    
    def _add(self, node: ast.AST, rule_id: str, message: str, severity: str = "MEDIUM", suggestion: str = ""):
        line = getattr(node, "lineno", 1) or 1
        col = getattr(node, "col_offset", 0) or 0
        snippet = self._lines[line - 1][:200] if 1 <= line <= len(self._lines) else ""
        self.findings.append(DynamicFinding(
            file=self.filename,
            line=line,
            col=col,
            category="resource_management",
            severity=severity,
            rule_id=rule_id,
            message=message,
            snippet=snippet,
            suggestion=suggestion
        ))
    
    def visit_Call(self, node: ast.Call):
        # 文件操作
        if isinstance(node.func, ast.Name) and node.func.id == 'open':
            # 检查是否在 with 语句中
            parent = getattr(node, '_parent', None)
            in_with = False
            current = node
            while current:
                if isinstance(current, ast.With):
                    in_with = True
                    break
                current = getattr(current, '_parent', None)
            
            if not in_with:
                self._add(node, "DYN-RES-001",
                         "文件打开未使用 with 语句，可能导致资源泄漏",
                         "HIGH",
                         "使用 with open(...) as f: 确保文件自动关闭")
        
        # 数据库连接
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ('connect', 'Connection'):
                db_keywords = ['mysql', 'postgres', 'sqlite', 'mongodb', 'redis', 'db', 'database']
                func_str = ast.unparse(node.func) if hasattr(ast, 'unparse') else str(node.func)
                if any(kw in func_str.lower() for kw in db_keywords):
                    self._add(node, "DYN-RES-002",
                             "数据库连接需要确保正确关闭",
                             "MEDIUM",
                             "使用连接池或 with 语句管理数据库连接")
        
        # Socket 操作
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id == 'socket' and
                node.func.attr in ('socket', 'connect', 'bind')):
                self._add(node, "DYN-RES-003",
                         "Socket 连接需要确保正确关闭",
                         "MEDIUM",
                         "在 finally 块中关闭 socket 或使用 with 语句")
        
        # Lock 操作
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ('Lock', 'RLock', 'Semaphore'):
                self._add(node, "DYN-RES-004",
                         "锁对象需要确保正确释放",
                         "HIGH",
                         "使用 with lock: 语句确保锁自动释放")
        
        self.generic_visit(node)


class ConcurrencyVisitor(ast.NodeVisitor):
    """并发与异步操作检测"""
    
    def __init__(self, code: str, filename: str):
        self.code = code
        self.filename = filename
        self.findings: List[DynamicFinding] = []
        self._lines = code.splitlines()
    
    def _add(self, node: ast.AST, rule_id: str, message: str, severity: str = "MEDIUM", suggestion: str = ""):
        line = getattr(node, "lineno", 1) or 1
        col = getattr(node, "col_offset", 0) or 0
        snippet = self._lines[line - 1][:200] if 1 <= line <= len(self._lines) else ""
        self.findings.append(DynamicFinding(
            file=self.filename,
            line=line,
            col=col,
            category="concurrency",
            severity=severity,
            rule_id=rule_id,
            message=message,
            snippet=snippet,
            suggestion=suggestion
        ))
    
    def visit_Call(self, node: ast.Call):
        # 多线程
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id == 'threading' and
                node.func.attr == 'Thread'):
                self._add(node, "DYN-CONC-001",
                         "创建线程，注意线程安全和资源竞争",
                         "MEDIUM",
                         "使用锁保护共享资源，考虑使用线程池")
        
        # 多进程
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id == 'multiprocessing' and
                node.func.attr == 'Process'):
                self._add(node, "DYN-CONC-002",
                         "创建进程，注意进程间通信和资源管理",
                         "MEDIUM",
                         "使用 Queue 或 Pipe 进行进程间通信，确保进程正确退出")
        
        # 异步操作
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ('gather', 'wait', 'create_task'):
                self._add(node, "DYN-CONC-003",
                         "异步操作需要正确处理异常和超时",
                         "MEDIUM",
                         "使用 try-except 捕获异常，设置超时限制")
        
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """检测异步函数"""
        # 检查是否有异常处理
        has_try = any(isinstance(n, ast.Try) for n in ast.walk(node))
        if not has_try:
            self._add(node, "DYN-CONC-004",
                     f"异步函数 {node.name} 缺少异常处理",
                     "LOW",
                     "添加 try-except 处理可能的异常")
        
        self.generic_visit(node)


class BoundaryConditionsVisitor(ast.NodeVisitor):
    """边界条件与异常处理检测"""
    
    def __init__(self, code: str, filename: str):
        self.code = code
        self.filename = filename
        self.findings: List[DynamicFinding] = []
        self._lines = code.splitlines()
    
    def _add(self, node: ast.AST, rule_id: str, message: str, severity: str = "MEDIUM", suggestion: str = ""):
        line = getattr(node, "lineno", 1) or 1
        col = getattr(node, "col_offset", 0) or 0
        snippet = self._lines[line - 1][:200] if 1 <= line <= len(self._lines) else ""
        self.findings.append(DynamicFinding(
            file=self.filename,
            line=line,
            col=col,
            category="boundary_conditions",
            severity=severity,
            rule_id=rule_id,
            message=message,
            snippet=snippet,
            suggestion=suggestion
        ))
    
    def visit_For(self, node: ast.For):
        """检测循环边界"""
        # 检查是否使用 range() 且可能越界
        if isinstance(node.iter, ast.Call):
            if isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                # 检查循环体中是否有数组访问
                for child in ast.walk(node):
                    if isinstance(child, ast.Subscript):
                        self._add(node, "DYN-BOUND-001",
                                 "循环中的数组访问可能越界",
                                 "MEDIUM",
                                 "确保索引在有效范围内，考虑使用 enumerate()")
                        break
        
        self.generic_visit(node)
    
    def visit_BinOp(self, node: ast.BinOp):
        """检测数值计算"""
        # 除法操作
        if isinstance(node.op, ast.Div):
            self._add(node, "DYN-BOUND-002",
                     "除法操作可能导致除零错误",
                     "MEDIUM",
                     "检查除数是否为零")
        
        # 幂运算
        if isinstance(node.op, ast.Pow):
            self._add(node, "DYN-BOUND-003",
                     "幂运算可能导致溢出",
                     "LOW",
                     "检查输入范围，防止数值溢出")
        
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """检测递归函数"""
        # 检查函数是否调用自己
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == node.name:
                    self._add(node, "DYN-BOUND-004",
                             f"递归函数 {node.name} 需要确保有终止条件",
                             "HIGH",
                             "添加递归深度限制和明确的终止条件")
                    break
        
        self.generic_visit(node)


class EnvironmentConfigVisitor(ast.NodeVisitor):
    """环境依赖与配置检测"""
    
    def __init__(self, code: str, filename: str):
        self.code = code
        self.filename = filename
        self.findings: List[DynamicFinding] = []
        self._lines = code.splitlines()
    
    def _add(self, node: ast.AST, rule_id: str, message: str, severity: str = "MEDIUM", suggestion: str = ""):
        line = getattr(node, "lineno", 1) or 1
        col = getattr(node, "col_offset", 0) or 0
        snippet = self._lines[line - 1][:200] if 1 <= line <= len(self._lines) else ""
        self.findings.append(DynamicFinding(
            file=self.filename,
            line=line,
            col=col,
            category="environment_config",
            severity=severity,
            rule_id=rule_id,
            message=message,
            snippet=snippet,
            suggestion=suggestion
        ))
    
    def visit_Call(self, node: ast.Call):
        # 环境变量
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id == 'os' and
                node.func.attr in ('getenv', 'environ')):
                self._add(node, "DYN-ENV-001",
                         "读取环境变量应提供默认值",
                         "LOW",
                         "使用 os.getenv(key, default) 提供默认值")
        
        # 配置文件读取
        if isinstance(node.func, ast.Attribute):
            config_methods = ['read', 'load', 'parse']
            if node.func.attr in config_methods:
                # 检查参数是否包含配置文件
                if node.args:
                    arg = node.args[0]
                    if isinstance(arg, ast.Constant):
                        val = str(arg.value).lower()
                        if any(ext in val for ext in ['.ini', '.cfg', '.conf', '.yaml', '.yml', '.json', '.toml']):
                            self._add(node, "DYN-ENV-002",
                                     "配置文件读取应处理文件不存在的情况",
                                     "MEDIUM",
                                     "使用 try-except 处理 FileNotFoundError")
        
        # 时间处理
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id in ('datetime', 'time') and
                node.func.attr in ('now', 'strftime', 'strptime')):
                self._add(node, "DYN-ENV-003",
                         "时间处理应考虑时区问题",
                         "LOW",
                         "使用 timezone-aware datetime 对象")
        
        self.generic_visit(node)


class DynamicExecutionVisitor(ast.NodeVisitor):
    """动态代码执行检测"""
    
    def __init__(self, code: str, filename: str):
        self.code = code
        self.filename = filename
        self.findings: List[DynamicFinding] = []
        self._lines = code.splitlines()
    
    def _add(self, node: ast.AST, rule_id: str, message: str, severity: str = "HIGH", suggestion: str = ""):
        line = getattr(node, "lineno", 1) or 1
        col = getattr(node, "col_offset", 0) or 0
        snippet = self._lines[line - 1][:200] if 1 <= line <= len(self._lines) else ""
        self.findings.append(DynamicFinding(
            file=self.filename,
            line=line,
            col=col,
            category="dynamic_execution",
            severity=severity,
            rule_id=rule_id,
            message=message,
            snippet=snippet,
            suggestion=suggestion
        ))
    
    def visit_Call(self, node: ast.Call):
        # eval() 和 exec()
        if isinstance(node.func, ast.Name):
            if node.func.id in ('eval', 'exec'):
                self._add(node, "DYN-EXEC-001",
                         f"使用 {node.func.id}() 存在代码注入风险",
                         "HIGH",
                         "避免使用 eval/exec，或严格验证输入")
            
            # compile()
            elif node.func.id == 'compile':
                self._add(node, "DYN-EXEC-002",
                         "使用 compile() 可能执行不可信代码",
                         "HIGH",
                         "验证编译的代码来源")
            
            # __import__()
            elif node.func.id == '__import__':
                self._add(node, "DYN-EXEC-003",
                         "动态导入模块可能引入安全风险",
                         "MEDIUM",
                         "使用 importlib 并验证模块名称")
        
        # pickle 反序列化
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id == 'pickle' and
                node.func.attr in ('loads', 'load')):
                self._add(node, "DYN-EXEC-004",
                         "pickle 反序列化可能执行恶意代码",
                         "HIGH",
                         "只反序列化可信来源的数据，考虑使用 JSON")
        
        # YAML unsafe load
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id == 'yaml' and
                node.func.attr == 'load'):
                # 检查是否使用 SafeLoader
                has_safe = False
                for kw in node.keywords:
                    if kw.arg == 'Loader':
                        if isinstance(kw.value, ast.Attribute) and 'Safe' in getattr(kw.value, 'attr', ''):
                            has_safe = True
                if not has_safe:
                    self._add(node, "DYN-EXEC-005",
                             "yaml.load() 未使用 SafeLoader 可能执行恶意代码",
                             "HIGH",
                             "使用 yaml.safe_load() 或 yaml.load(..., Loader=yaml.SafeLoader)")
        
        # getattr/setattr with dynamic strings
        if isinstance(node.func, ast.Name):
            if node.func.id in ('getattr', 'setattr'):
                if node.args and len(node.args) >= 2:
                    # 检查属性名是否动态生成
                    if not isinstance(node.args[1], ast.Constant):
                        self._add(node, "DYN-EXEC-006",
                                 f"{node.func.id}() 使用动态属性名可能不安全",
                                 "MEDIUM",
                                 "验证属性名在白名单中")
        
        self.generic_visit(node)


class JavaDynamicDetector(DynamicDetector):
    """Java 动态检测器"""
    
    def __init__(self, files: List[Dict[str, Any]]):
        super().__init__(files)
        self.file_map: Dict[str, str] = {}
        for f in files:
            name = f.get("file") or f.get("path") or ""
            if name.endswith('.java'):
                self.file_map[name] = f.get("content", "")
    
    def detect_user_input(self):
        """检测 Java 中的用户输入"""
        for filename, content in self.file_map.items():
            lines = content.splitlines()
            
            # HTTP 请求参数
            for i, line in enumerate(lines, 1):
                if re.search(r'request\.(getParameter|getHeader|getCookie)', line):
                    self.findings.append(DynamicFinding(
                        file=filename, line=i,
                        category="user_input",
                        severity="HIGH",
                        rule_id="JAVA-DYN-001",
                        message="获取 HTTP 请求参数需要验证和清理",
                        snippet=line.strip()[:200],
                        suggestion="使用白名单验证，防止注入攻击"
                    ))
            
            # JSON/XML 反序列化
            for i, line in enumerate(lines, 1):
                if re.search(r'(Jackson|Gson|JSON|XMLDecoder)\.(readValue|fromJson|decode)', line):
                    self.findings.append(DynamicFinding(
                        file=filename, line=i,
                        category="user_input",
                        severity="MEDIUM",
                        rule_id="JAVA-DYN-002",
                        message="JSON/XML 反序列化需要验证数据来源",
                        snippet=line.strip()[:200],
                        suggestion="限制可反序列化的类，使用白名单"
                    ))
    
    def detect_resource_management(self):
        """检测 Java 资源管理"""
        for filename, content in self.file_map.items():
            lines = content.splitlines()
            
            # 检查是否使用 try-with-resources
            for i, line in enumerate(lines, 1):
                if re.search(r'new\s+(FileInputStream|FileOutputStream|BufferedReader|Connection|Socket)', line):
                    # 检查上下文是否有 try-with-resources
                    context = '\n'.join(lines[max(0, i-3):min(len(lines), i+3)])
                    if 'try' not in context or 'try (' not in context:
                        self.findings.append(DynamicFinding(
                            file=filename, line=i,
                            category="resource_management",
                            severity="HIGH",
                            rule_id="JAVA-DYN-003",
                            message="资源未使用 try-with-resources，可能泄漏",
                            snippet=line.strip()[:200],
                            suggestion="使用 try (Resource r = new Resource()) {...}"
                        ))
    
    def detect_concurrency(self):
        """检测 Java 并发"""
        for filename, content in self.file_map.items():
            lines = content.splitlines()
            
            # 线程创建
            for i, line in enumerate(lines, 1):
                if re.search(r'new\s+Thread\s*\(', line):
                    self.findings.append(DynamicFinding(
                        file=filename, line=i,
                        category="concurrency",
                        severity="MEDIUM",
                        rule_id="JAVA-DYN-004",
                        message="创建线程需要考虑线程安全",
                        snippet=line.strip()[:200],
                        suggestion="使用 ExecutorService 线程池"
                    ))
            
            # synchronized 块
            for i, line in enumerate(lines, 1):
                if 'synchronized' in line and '(' in line:
                    self.findings.append(DynamicFinding(
                        file=filename, line=i,
                        category="concurrency",
                        severity="LOW",
                        rule_id="JAVA-DYN-005",
                        message="synchronized 块需要注意死锁风险",
                        snippet=line.strip()[:200],
                        suggestion="避免嵌套锁，使用 java.util.concurrent"
                    ))
    
    def detect_dynamic_execution(self):
        """检测 Java 动态执行"""
        for filename, content in self.file_map.items():
            lines = content.splitlines()
            
            # 反射
            for i, line in enumerate(lines, 1):
                if re.search(r'Class\.forName|\.getDeclaredMethod|\.invoke', line):
                    self.findings.append(DynamicFinding(
                        file=filename, line=i,
                        category="dynamic_execution",
                        severity="HIGH",
                        rule_id="JAVA-DYN-006",
                        message="使用反射可能绕过安全检查",
                        snippet=line.strip()[:200],
                        suggestion="限制反射使用，验证类名和方法名"
                    ))


class CppDynamicDetector(DynamicDetector):
    """C/C++ 动态检测器"""
    
    def __init__(self, files: List[Dict[str, Any]]):
        super().__init__(files)
        self.file_map: Dict[str, str] = {}
        for f in files:
            name = f.get("file") or f.get("path") or ""
            if name.endswith(('.c', '.cpp', '.cc', '.cxx')):
                self.file_map[name] = f.get("content", "")
    
    def detect_user_input(self):
        """检测 C/C++ 用户输入"""
        for filename, content in self.file_map.items():
            lines = content.splitlines()
            
            # gets, scanf 等不安全函数
            for i, line in enumerate(lines, 1):
                if re.search(r'\b(gets|scanf|vscanf)\s*\(', line):
                    self.findings.append(DynamicFinding(
                        file=filename, line=i,
                        category="user_input",
                        severity="HIGH",
                        rule_id="CPP-DYN-001",
                        message="使用不安全的输入函数",
                        snippet=line.strip()[:200],
                        suggestion="使用 fgets 或 scanf_s 等安全函数"
                    ))
    
    def detect_resource_management(self):
        """检测 C/C++ 资源管理"""
        for filename, content in self.file_map.items():
            lines = content.splitlines()
            
            # malloc/free 配对检查
            for i, line in enumerate(lines, 1):
                if re.search(r'\b(malloc|calloc|realloc)\s*\(', line):
                    self.findings.append(DynamicFinding(
                        file=filename, line=i,
                        category="resource_management",
                        severity="MEDIUM",
                        rule_id="CPP-DYN-002",
                        message="动态内存分配需要确保释放",
                        snippet=line.strip()[:200],
                        suggestion="确保调用 free()，或使用 RAII 模式"
                    ))
            
            # fopen/fclose 配对
            for i, line in enumerate(lines, 1):
                if re.search(r'\bfopen\s*\(', line):
                    self.findings.append(DynamicFinding(
                        file=filename, line=i,
                        category="resource_management",
                        severity="MEDIUM",
                        rule_id="CPP-DYN-003",
                        message="文件打开需要确保关闭",
                        snippet=line.strip()[:200],
                        suggestion="确保调用 fclose()"
                    ))
    
    def detect_boundary_conditions(self):
        """检测 C/C++ 边界条件"""
        for filename, content in self.file_map.items():
            lines = content.splitlines()
            
            # 数组访问
            for i, line in enumerate(lines, 1):
                if re.search(r'\[\s*\w+\s*\]', line) and 'for' in line:
                    self.findings.append(DynamicFinding(
                        file=filename, line=i,
                        category="boundary_conditions",
                        severity="MEDIUM",
                        rule_id="CPP-DYN-004",
                        message="循环中的数组访问需要边界检查",
                        snippet=line.strip()[:200],
                        suggestion="确保索引在 [0, size) 范围内"
                    ))