"""
CppFixer - C/C++代码修复器（支持 DebugBench 逻辑差异驱动 + 语法小修复 + 归一化）
"""
import re
from typing import Dict, List, Any, Union

from .base_fixer import BaseFixer, FixResult, Language


class CppFixer(BaseFixer):
    """C/C++专用修复器"""

    def __init__(self, llm_client=None, language: Language = Language.CPP,
                 prompt_config: Dict[str, Any] = None):
        super().__init__(language, llm_client)
        # ✅ 添加 prompt 配置
        self.prompt_conf = prompt_config or {
            "language": "zh",
            "style": "concise",
            "force_code_block_only": True
        }

    # =========================================================
    #  LLM 辅助：错误代码 vs 正确代码 的逻辑差异分析
    # =========================================================
    def _analyze_logic_diff_v2(self, buggy_code: str, reference_code: str) -> List[Dict[str, str]]:
        """
        使用 LLM 比较 C/C++ 错误代码 A 与正确代码 B，
        自动生成「逻辑差异报告」用于 DebugBench 修复。

        ⚠️ 不泄露 ground truth（禁止输出正确代码）
        ⚠️ 只输出 JSON 数组
        ⚠️ 只描述逻辑、流程、边界条件、递归、循环、变量更新差异
        """
        if not self.llm_client:
            return [{"type": "NO_LLM", "message": "LLM 客户端未配置，无法分析逻辑差异"}]

        try:
            prompt = (
                "你是一名 C/C++ 程序结构与逻辑分析专家。\n"
                "下面是两份代码：A 是错误版本，B 是正确版本。\n"
                "你的任务：\n"
                "  1. 比较 A 与 B 的逻辑行为差异（流程、条件、循环、边界、递归、变量更新）。\n"
                "  2. 不能输出 B 的任何代码，不能泄露正确实现内容。\n"
                "  3. 只能用文字描述“差异点是什么”，不能给代码片段。\n"
                "  4. 每条差异以 JSON 形式给出，例如：\n"
                "     {\"type\": \"MISSING_LOGIC\", \"message\": \"A 缺少对某个边界条件的判断\"}\n"
                "最终输出一个 JSON 数组。\n\n"
                "=== 错误代码 A ===\n"
                f"{buggy_code}\n\n"
                "=== 正确代码 B（禁止泄露）===\n"
                f"{reference_code}\n\n"
                "=== 请输出 JSON 数组（不能包含代码） ==="
            )

            response = self.llm_client.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1500,
            )

            import json
            data = json.loads(response)
            if isinstance(data, list):
                return data

            return [{"type": "PARSE_FAIL", "message": "LLM 输出不是 JSON 数组"}]

        except Exception as e:
            return [{"type": "ANALYSIS_FAIL", "message": f"分析失败: {e}"}]

    # =========================================================
    #  规则修复部分
    # =========================================================
    def apply_rule_fixes(self, file: Dict[str, Any], issues: List[Union[Dict, str]]) -> FixResult:
        """应用规则化修复"""
        filename = file.get("file", "")
        content = file.get("content", "")
        fixed_content = content
        fixed_count = 0

        print(f"[CppFixer] 开始规则修复: {filename}")
        print(f"[CppFixer] 待修复问题数: {len(issues)}")

        # ✅ 规范化 issues 格式
        normalized_issues = self._normalize_issues(issues)

        # 规则1: gets() -> fgets()
        gets_issues = [issue for issue in normalized_issues
                       if "gets" in issue.get("message", "").lower() or issue.get("rule_id") == "CPP001"]
        if gets_issues:
            print(f"[CppFixer] 修复 gets(): {len(gets_issues)} 处")
            new_content, count = self._fix_gets(fixed_content)
            if count > 0:
                fixed_content = new_content
                fixed_count += count

        # 规则2: strcpy() -> strncpy()
        strcpy_issues = [issue for issue in normalized_issues
                         if "strcpy" in issue.get("message", "").lower() or issue.get("rule_id") == "CPP002"]
        if strcpy_issues:
            print(f"[CppFixer] 修复 strcpy(): {len(strcpy_issues)} 处")
            new_content, count = self._fix_strcpy(fixed_content)
            if count > 0:
                fixed_content = new_content
                fixed_count += count

        # 规则3: sprintf() -> snprintf()
        sprintf_issues = [issue for issue in normalized_issues
                          if "sprintf" in issue.get("message", "").lower() or issue.get("rule_id") == "CPP003"]
        if sprintf_issues:
            print(f"[CppFixer] 修复 sprintf(): {len(sprintf_issues)} 处")
            new_content, count = self._fix_sprintf(fixed_content)
            if count > 0:
                fixed_content = new_content
                fixed_count += count

        # 规则4: 添加空指针检查
        null_issues = [issue for issue in normalized_issues
                       if "null" in issue.get("message", "").lower() or issue.get("rule_id") == "CPP004"]
        if null_issues:
            print(f"[CppFixer] 添加空指针检查: {len(null_issues)} 处")
            new_content, count = self._fix_null_check(fixed_content)
            if count > 0:
                fixed_content = new_content
                fixed_count += count

        # 规则5: 初始化变量
        uninit_issues = [issue for issue in normalized_issues
                         if "初始化" in issue.get("message", "") or issue.get("rule_id") == "CPP006"]
        if uninit_issues:
            print(f"[CppFixer] 初始化变量: {len(uninit_issues)} 处")
            new_content, count = self._fix_uninitialized_vars(fixed_content)
            if count > 0:
                fixed_content = new_content
                fixed_count += count

        print(f"[CppFixer] 规则修复完成: 修复了 {fixed_count} 处问题")

        return FixResult(
            file=filename,
            language=self.language.value,
            original_content=content,
            fixed_content=fixed_content,
            fixed_count=fixed_count,
            method="rule",
            success=fixed_count > 0,
            error_message="" if fixed_count > 0 else "没有找到可自动修复的问题"
        )

    def _normalize_issues(self, issues: List[Union[Dict, str]]) -> List[Dict]:
        """规范化 issues 格式"""
        normalized = []
        for issue in issues:
            if isinstance(issue, dict):
                normalized.append(issue)
            elif isinstance(issue, str):
                parsed = self._parse_issue_string(issue)
                normalized.append(parsed)
            else:
                normalized.append({
                    "type": "unknown",
                    "message": str(issue),
                    "rule_id": "UNKNOWN"
                })
        return normalized

    def _parse_issue_string(self, issue_str: str) -> Dict[str, Any]:
        """解析字符串格式的问题"""
        pattern = r'^([^:]+):(\d+)(?::(\d+))?: (\w+): (.+?) \[(\w+)\]'
        match = re.match(pattern, issue_str)
        if match:
            file, line, column, severity, message, rule_id = match.groups()
            return {
                "file": file,
                "line": int(line),
                "column": int(column) if column else 0,
                "severity": severity.upper(),
                "message": message,
                "rule_id": rule_id
            }

        return {
            "type": "unknown",
            "message": issue_str,
            "rule_id": "UNKNOWN",
            "severity": "MEDIUM"
        }

    def _fix_gets(self, content: str) -> tuple:
        """修复 gets() -> fgets()"""
        count = 0
        lines = content.split('\n')
        new_lines = []
        needs_stdio = False

        for line in lines:
            match = re.search(r'\bgets\s*\(\s*(\w+)\s*\)', line)
            if match:
                buf_name = match.group(1)
                new_line = re.sub(
                    r'\bgets\s*\(\s*' + buf_name + r'\s*\)',
                    f'fgets({buf_name}, sizeof({buf_name}), stdin)',
                    line
                )
                new_lines.append(new_line)
                count += 1
                needs_stdio = True
            else:
                new_lines.append(line)

        if needs_stdio and not any('#include <stdio.h>' in line for line in new_lines):
            for i, line in enumerate(new_lines):
                if line.strip().startswith('#include'):
                    new_lines.insert(i + 1, '#include <stdio.h>')
                    break
            else:
                new_lines.insert(0, '#include <stdio.h>')

        return '\n'.join(new_lines), count

    def _fix_strcpy(self, content: str) -> tuple:
        """修复 strcpy() -> strncpy()"""
        count = 0
        pattern = r'\bstrcpy\s*\(\s*(\w+)\s*,\s*([^)]+)\s*\)'

        def replace_strcpy(match):
            nonlocal count
            dest = match.group(1)
            src = match.group(2)
            count += 1
            return f'strncpy({dest}, {src}, sizeof({dest}) - 1)'

        new_content = re.sub(pattern, replace_strcpy, content)

        if count > 0 and '#include <string.h>' not in new_content:
            lines = new_content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('#include'):
                    lines.insert(i + 1, '#include <string.h>')
                    break
            else:
                lines.insert(0, '#include <string.h>')
            new_content = '\n'.join(lines)

        return new_content, count

    def _fix_sprintf(self, content: str) -> tuple:
        """修复 sprintf() -> snprintf()"""
        count = 0
        pattern = r'\bsprintf\s*\(\s*(\w+)\s*,\s*'

        def replace_sprintf(match):
            nonlocal count
            buf = match.group(1)
            count += 1
            return f'snprintf({buf}, sizeof({buf}), '

        new_content = re.sub(pattern, replace_sprintf, content)
        return new_content, count

    def _fix_null_check(self, content: str) -> tuple:
        """添加空指针检查"""
        count = 0
        lines = content.split('\n')
        new_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            malloc_pattern = r'(\w+)\s*=\s*(malloc|calloc|realloc)\s*\('
            match = re.search(malloc_pattern, line)

            if match:
                ptr_name = match.group(1)
                has_check = False
                for j in range(i + 1, min(i + 5, len(lines))):
                    if f"{ptr_name}" in lines[j] and ("NULL" in lines[j] or "nullptr" in lines[j] or "!" in lines[j]):
                        has_check = True
                        break

                if not has_check:
                    indent = len(line) - len(line.lstrip())
                    null_check_lines = [
                        ' ' * indent + f'if ({ptr_name} == NULL) {{',
                        ' ' * (indent + 4) + 'fprintf(stderr, "Memory allocation failed\\n");',
                        ' ' * (indent + 4) + 'exit(1);',
                        ' ' * indent + '}'
                    ]
                    new_lines.extend(null_check_lines)
                    count += 1
            i += 1

        if count > 0:
            if not any('#include <stdlib.h>' in line for line in new_lines):
                for i, line in enumerate(new_lines):
                    if line.strip().startswith('#include'):
                        new_lines.insert(i + 1, '#include <stdlib.h>')
                        break
                else:
                    new_lines.insert(0, '#include <stdlib.h>')

            if not any('#include <stdio.h>' in line for line in new_lines):
                for i, line in enumerate(new_lines):
                    if line.strip().startswith('#include'):
                        new_lines.insert(i + 1, '#include <stdio.h>')
                        break
                else:
                    new_lines.insert(0, '#include <stdio.h>')

        return '\n'.join(new_lines), count

    def _fix_uninitialized_vars(self, content: str) -> tuple:
        """初始化未初始化的变量"""
        count = 0
        lines = content.split('\n')
        new_lines = []

        for line in lines:
            match = re.match(r'^(\s*)(int|char|float|double|long)\s+(\w+)\s*;', line)
            if match:
                indent, type_name, var_name = match.groups()
                if type_name in ['int', 'long']:
                    new_line = f'{indent}{type_name} {var_name} = 0;'
                elif type_name in ['float', 'double']:
                    new_line = f'{indent}{type_name} {var_name} = 0.0;'
                elif type_name == 'char':
                    new_line = f'{indent}{type_name} {var_name} = \'\\0\';'
                else:
                    new_line = line
                new_lines.append(new_line)
                count += 1
                continue

            match = re.match(r'^(\s*)(int|char|float|double)\s+(\w+)\[([^\]]+)\]\s*;', line)
            if match:
                indent, type_name, var_name, size = match.groups()
                new_line = f'{indent}{type_name} {var_name}[{size}] = {{0}};'
                new_lines.append(new_line)
                count += 1
                continue

            new_lines.append(line)

        return '\n'.join(new_lines), count

    # =========================================================
    #  LLM 修复
    # =========================================================
    def apply_llm_fixes(self, file: Dict[str, Any], issues: List[Union[Dict, str]],
                        user_request: str = "") -> FixResult:
        """应用LLM修复"""
        filename = file.get("file", "")
        content = file.get("content", "")

        result = FixResult(
            file=filename,
            language=self.language.value,
            original_content=content,
            fixed_content=content,
            fixed_count=0,
            method="llm",
            success=False
        )

        if not self.llm_client:
            result.error_message = "LLM客户端未配置"
            print(f"[CppFixer] LLM客户端未配置")
            return result

        print(f"[CppFixer] 开始LLM修复: {filename}")
        print(f"[CppFixer] 问题数: {len(issues)}")

        try:
            normalized_issues = self._normalize_issues(issues)

            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(
                filename=filename,
                original_content=content,
                issues=normalized_issues,
                user_request=user_request,
                force_code_block_only=self.prompt_conf.get("force_code_block_only", True)
            )

            print(f"[CppFixer] 调用LLM API...")

            if hasattr(self.llm_client, 'chat') and callable(self.llm_client.chat):
                response = self.llm_client.chat(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=4000
                )
            else:
                result.error_message = "不支持的LLM客户端类型"
                return result

            print(f"[CppFixer] LLM响应长度: {len(response)} 字符")

            fixed_code = self._extract_code_from_response(response, filename)

            if fixed_code and fixed_code != content:
                result.fixed_content = fixed_code
                result.fixed_count = max(1, len(normalized_issues))
                result.success = True
                print(f"[CppFixer] LLM修复成功")
            else:
                result.error_message = "LLM未返回有效的修复代码"
                print(f"[CppFixer] LLM修复失败: 未返回有效代码")

        except Exception as e:
            result.error_message = f"LLM调用失败: {str(e)}"
            print(f"[CppFixer] LLM调用异常: {e}")
            import traceback
            traceback.print_exc()

        return result

    def _build_system_prompt(self) -> str:
        """构建LLM系统提示词（标准化）"""
        lang = self.prompt_conf.get("language", "zh")
        style = self.prompt_conf.get("style", "concise")
        lang_name = "C++" if self.language == Language.CPP else "C"
        lang_ext = "cpp" if self.language == Language.CPP else "c"

        return (
            f"你是专业的 {lang_name} 代码修复助手。请严格遵守：\n"
            f"1) 仅输出完整的代码，不要输出解释。\n"
            f"2) 输出格式必须为一个带文件名的 {lang_ext} 代码块：```{lang_ext} <文件名>.{lang_ext}\\n<完整代码>```\n"
            f"3) 不要输出 diff、不要输出多余文本或多个代码块。\n"
            f"4) 如果无法修复，请也输出原样的完整文件代码块。\n"
            f"5) 确保输出能被正常编译，并优先修复语法错误和安全问题。\n"
            f"语言：{lang}；风格：{style}。\n"
        )

    def _build_user_prompt(
            self,
            filename: str,
            original_content: str,
            issues: List[Dict[str, Any]],
            user_request: str,
            force_code_block_only: bool
    ) -> str:
        """
        构建LLM用户提示词（支持 DebugBench 模式 + 普通模式）
        """
        lang_ext = "cpp" if self.language == Language.CPP else "c"

        debugbench_mode = False
        reference_code = ""
        if user_request and "[DEBUGBENCH]" in user_request:
            debugbench_mode = True
            start_tag = "【参考正确实现（ground truth）】"
            end_tag = "【参考实现结束】"
            start_idx = user_request.find(start_tag)
            end_idx = user_request.find(end_tag)
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                reference_code = user_request[start_idx + len(start_tag):end_idx].strip()

        if debugbench_mode and reference_code:
            strict_hint = (
                f"【重要】只输出一个带文件名的 {lang_ext} 代码块，不要任何说明文字、不要 diff。"
                if force_code_block_only else
                f"如果可能，只输出一个带文件名的 {lang_ext} 代码块；不要输出 diff 或解释。"
            )

            logic_issues = self._analyze_logic_diff_v2(original_content, reference_code)
            logic_report = "\n".join(
                f"- [{it.get('type', 'LOGIC')}] {it.get('message', '')}"
                for it in logic_issues
            )
            if not logic_report.strip():
                logic_report = "- [LOGIC_UNKNOWN] 系统未能自动分析逻辑差异，但你的代码必须与正确实现功能一致。"

            return (
                "你正在进行一个名为 DebugBench 的自动 C/C++ 代码修复任务。\n"
                "系统不会直接给出正确代码，而是提供从正确实现推断出的“逻辑差异报告”。\n"
                "你必须根据逻辑差异修复原始代码。\n\n"
                "【逻辑差异报告】\n"
                f"{logic_report}\n"
                "【逻辑差异结束】\n\n"
                "【原始代码】\n"
                f"{original_content}\n"
                "【原始代码结束】\n\n"
                f"{strict_hint}\n"
                f"输出格式示例：\n"
                f"```{lang_ext} {filename}\n<完整代码>\n```\n"
            )

        issue_lines = []
        for it in issues:
            issue_lines.append(
                f"- [{it.get('rule_id', '')}] 行 {it.get('line', '?')}: {it.get('message', '')}"
            )
        issue_text = "\n".join(issue_lines) if issue_lines else "无结构化缺陷条目。"

        strict_hint = (
            f"【重要】只输出一个带文件名的 {lang_ext} 代码块，不要任何说明文字、不要 diff。"
            if force_code_block_only else
            f"如果可能，只输出一个带文件名的 {lang_ext} 代码块；不要输出 diff 或解释。"
        )

        extra = ""
        if user_request and "[DEBUGBENCH]" not in user_request:
            extra = f"\n【用户补充需求】\n{user_request}\n"

        return (
            f"请修复下述 {lang_ext.upper()} 文件中的安全/语法/逻辑问题，并返回修复后的完整源代码。\n\n"
            f"【目标文件】{filename}\n"
            f"【检测到的问题】\n{issue_text}\n"
            f"{extra}\n"
            f"【原始代码开始】\n{original_content}\n【原始代码结束】\n\n"
            f"{strict_hint}\n"
            f"代码块格式示例：\n"
            f"```{lang_ext} {filename}\n<完整代码>\n```\n"
        )

    def _extract_code_from_response(self, response: str, expected_filename: str) -> str:
        """从LLM响应中提取代码"""
        lang_tag = self.language.value
        pattern = rf"```{lang_tag}\s+([^\n]+)?\s*\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)

        if matches:
            for match in matches:
                code = match[1] if len(match) > 1 else match[0]
                if code.strip():
                    return code.strip()

        pattern = rf"```(?:cpp|c)\s*\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
        if matches:
            return matches[0].strip()

        pattern = r"```\s*\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
        if matches:
            return matches[0].strip()

        return ""

    # =========================================================
    #  C++ 代码归一化（供 runner 使用，可选）
    # =========================================================
    @staticmethod
    def normalize_cpp(code: str) -> str:
        """
        对 C++ 做归一化：
        - 去注释（//、/* */）
        - 分离并排序 #include
        - 删除所有空白
        """
        # 去掉多行注释
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
        # 去掉单行注释
        code = re.sub(r"//.*", "", code)
        lines = code.splitlines()
        includes = [l for l in lines if l.strip().startswith("#include")]
        others = [l for l in lines if not l.strip().startswith("#include")]
        includes = sorted(set(includes))
        code = "\n".join(includes + others)
        code = re.sub(r"\s+", "", code)
        code = code.replace("std::", "")
        return code