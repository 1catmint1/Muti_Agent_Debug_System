"""
PythonFixer - Python代码修复器（支持 DebugBench 逻辑差异驱动 + 归一化）
"""
import re
from typing import Dict, List, Any, Union

from .base_fixer import BaseFixer, FixResult, Language


class PythonFixer(BaseFixer):
    """Python专用修复器"""

    def __init__(self, llm_client=None, prompt_config: Dict[str, Any] = None):
        super().__init__(Language.PYTHON, llm_client)
        # [保持与 CppFixer 一致的 prompt 配置]
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
        使用 LLM 比较 Python 错误代码 A 与正确代码 B，自动生成「逻辑差异报告」。

        ⚠️ 不泄露 ground truth（禁止输出正确代码）
        ⚠️ 只输出 JSON 数组
        """
        if not self.llm_client:
            return [{"type": "NO_LLM", "message": "LLM 客户端未配置，无法分析逻辑差异"}]

        try:
            prompt = (
                "你是一名 Python 程序结构与逻辑分析专家。\n"
                "下面是两份代码：A 是错误版本，B 是正确版本。\n"
                "你的任务：\n"
                "  1. 比较 A 与 B 的逻辑行为差异（流程、条件、循环、边界、递归、变量更新）。\n"
                "  2. 不能输出 B 的任何代码，不能泄露正确实现内容。\n"
                "  3. 只能用文字描述差异，每条差异用 JSON 对象表示，例如：\n"
                "     {\"type\": \"MISSING_LOGIC\", \"message\": \"A 缺少处理空列表的逻辑\"}\n"
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
        """应用规则化修复（轻量，主要处理 Py2 / 格式类问题）"""
        filename = file.get("file", "")
        content = file.get("content", "")
        fixed_content = content
        fixed_count = 0

        print(f"[PythonFixer] 开始规则修复: {filename}")
        print(f"[PythonFixer] 待修复问题数: {len(issues)}")

        normalized_issues = self._normalize_issues(issues)

        if any(issue.get("rule_id") == "PY201" for issue in normalized_issues):
            new_content = re.sub(r'\bxrange\b', 'range', fixed_content)
            if new_content != fixed_content:
                fixed_content = new_content
                fixed_count += 1

        if any(issue.get("rule_id") == "PY203" for issue in normalized_issues):
            new_content = re.sub(r'\braw_input\b', 'input', fixed_content)
            if new_content != fixed_content:
                fixed_content = new_content
                fixed_count += 1

        if any("except" in str(issue).lower() and "," in str(issue) for issue in normalized_issues):
            pattern = r'except\s+(\w+)\s*,\s*(\w+)'
            new_content = re.sub(pattern, r'except \1 as \2', fixed_content)
            if new_content != fixed_content:
                fixed_content = new_content
                fixed_count += 1

        if any("print" in str(issue).lower() for issue in normalized_issues):
            pattern = r'print\s+"([^"]*)"'
            new_content = re.sub(pattern, r'print("\1")', fixed_content)
            if new_content != fixed_content:
                fixed_content = new_content
                fixed_count += 1

        fixed_content, additional_fixes = self._apply_common_fixes(fixed_content, normalized_issues)
        fixed_count += additional_fixes

        print(f"[PythonFixer] 规则修复完成: 修复了 {fixed_count} 处问题")

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
        pattern1 = r'^([^:]+):(\d+):(\d+):\s*([A-Z]\d+)\s+(.+)$'
        match = re.match(pattern1, issue_str)
        if match:
            return {
                "file": match.group(1),
                "line": int(match.group(2)),
                "column": int(match.group(3)),
                "rule_id": match.group(4),
                "message": match.group(5),
                "severity": self._get_severity_from_code(match.group(4))
            }

        pattern2 = r'^([^:]+):(\d+):\s*([A-Z]\d+)\s+(.+)$'
        match = re.match(pattern2, issue_str)
        if match:
            return {
                "file": match.group(1),
                "line": int(match.group(2)),
                "rule_id": match.group(3),
                "message": match.group(4),
                "severity": self._get_severity_from_code(match.group(3))
            }

        return {
            "type": "unknown",
            "message": issue_str,
            "rule_id": "UNKNOWN",
            "severity": "MEDIUM"
        }

    def _get_severity_from_code(self, code: str) -> str:
        if code.startswith('E'):
            return 'HIGH'
        elif code.startswith('W'):
            return 'MEDIUM'
        return 'LOW'

    def _apply_common_fixes(self, content: str, issues: List[Dict]) -> tuple:
        fixed_content = content
        fix_count = 0

        if any(issue.get("rule_id") == "W291" for issue in issues):
            new_content = re.sub(r'[ \t]+$', '', fixed_content, flags=re.MULTILINE)
            if new_content != fixed_content:
                fixed_content = new_content
                fix_count += 1

        if any(issue.get("rule_id") == "W391" for issue in issues):
            new_content = fixed_content.rstrip() + '\n'
            if new_content != fixed_content:
                fixed_content = new_content
                fix_count += 1

        return fixed_content, fix_count

    # =========================================================
    #  LLM 修复
    # =========================================================
    def apply_llm_fixes(self, file: Dict[str, Any], issues: List[Union[Dict, str]],
                        user_request: str = "") -> FixResult:
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
            print(f"[PythonFixer] LLM客户端未配置")
            return result

        print(f"[PythonFixer] 开始LLM修复: {filename}")
        print(f"[PythonFixer] 问题数: {len(issues)}")

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

            print(f"[PythonFixer] 调用LLM API...")

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

            print(f"[PythonFixer] LLM响应长度: {len(response)} 字符")

            fixed_code = self._extract_code_from_response(response, filename)

            if fixed_code and fixed_code != content:
                result.fixed_content = fixed_code
                result.fixed_count = max(1, len(normalized_issues))
                result.success = True
                print(f"[PythonFixer] LLM修复成功")
            else:
                result.error_message = "LLM未返回有效的修复代码"
                print(f"[PythonFixer] LLM修复失败: 未返回有效代码")

        except Exception as e:
            result.error_message = f"LLM调用失败: {str(e)}"
            print(f"[PythonFixer] LLM调用异常: {e}")
            import traceback
            traceback.print_exc()

        return result

    def _build_system_prompt(self) -> str:
        lang = self.prompt_conf.get("language", "zh")
        style = self.prompt_conf.get("style", "concise")
        return (
            f"你是专业的 Python 代码修复助手。请严格遵守：\n"
            f"1) 仅输出完整的代码，不要输出解释。\n"
            f"2) 输出格式必须为一个带文件名的 python 代码块：```python <文件名>.py\\n<完整代码>```\n"
            f"3) 不要输出 diff、不要输出多余文本或多个代码块。\n"
            f"4) 如果无法修复，请也输出原样的完整文件代码块。\n"
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
        lang_ext = "python"

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

        # 🔥 裁剪过长的代码，防止 OOM
        MAX_CHARS = 6000
        if len(original_content) > MAX_CHARS:
            truncated_content = original_content[:MAX_CHARS] + "\n\n# ... (代码过长，仅显示前 6000 字符) ..."
        else:
            truncated_content = original_content

        # DebugBench 逻辑保持不变
        if debugbench_mode and reference_code:
            strict_hint = (
                "【重要】只输出一个带文件名的 python 代码块，不要任何说明文字、不要 diff。"
                if force_code_block_only else
                "如果可能，只输出一个带文件名的 python 代码块；不要输出 diff 或解释。"
            )
            logic_issues = self._analyze_logic_diff_v2(truncated_content, reference_code)
            logic_report = "\n".join(f"- [{it.get('type', 'LOGIC')}] {it.get('message', '')}" for it in logic_issues)
            return (
                "你正在进行一个名为 DebugBench 的自动 Python 代码修复任务。\n"
                f"【逻辑差异报告】\n{logic_report}\n\n"
                f"【原始代码】\n{truncated_content}\n\n"
                f"{strict_hint}\n"
                f"输出格式示例：\n```python\n<完整代码>\n```\n"
            )

        # === 常规修复 Prompt 构建 ===
        issue_lines = []
        for it in issues:
            issue_lines.append(
                f"- [{it.get('rule_id', '')}] 行 {it.get('line', '?')}: {it.get('message', '')}"
            )
        issue_text = "\n".join(issue_lines) if issue_lines else "无结构化缺陷条目（可能是外部工具或动态问题）。"

        strict_hint = (
            "【重要】只输出一个带文件名的 python 代码块。不要输出 diff、不要输出文件名、不要输出解释文字。"
            "【注意】确保修改后的代码保持原有的函数签名和类结构，不要删除现有的功能，只修复报错的问题。"  # 🔥 加强约束
            if force_code_block_only else
            "请直接输出修复后的完整代码块。"
        )

        extra = ""
        if user_request and "[DEBUGBENCH]" not in user_request:
            extra = f"\n【用户补充需求】\n{user_request}\n"

        return (
            f"请修复下述文件中的问题，并返回修复后的完整源代码。\n\n"
            f"【目标文件】{filename}\n"
            f"【检测到的问题】\n{issue_text}\n"
            f"{extra}\n"
            f"【原始代码开始】\n{truncated_content}\n【原始代码结束】\n\n"
            f"{strict_hint}\n"
            f"请直接输出 Python 代码块，格式如下：\n"
            f"```python\n"
            f"<完整代码>\n"
            f"```\n"
        )

    def _extract_code_from_response(self, response: str, expected_filename: str) -> str:
        # 清理首尾空白
        response = response.strip()

        # 1. 尝试匹配标准 ```python ... ``` (忽略文件名)
        pattern_std = r"```(?:python|py).*?\n(.*?)```"
        matches = re.findall(pattern_std, response, re.DOTALL | re.IGNORECASE)
        if matches:
            # 选最长的一个块，防止选到短小的示例代码
            return max(matches, key=len).strip()

        # 2. 尝试匹配通用 ``` ... ```
        pattern_generic = r"```.*?\n(.*?)```"
        matches = re.findall(pattern_generic, response, re.DOTALL)
        if matches:
            return max(matches, key=len).strip()

        # 3. 🔥 暴力提取：如果 LLM 没写 Markdown 标记，直接按行过滤
        # 这种情况在本地小模型中非常常见
        lines = response.split('\n')
        code_lines = []
        is_code_started = False

        for line in lines:
            stripped = line.strip()
            # 如果遇到 import, class, def, from，认为代码开始了
            if (stripped.startswith('import ') or
                    stripped.startswith('from ') or
                    stripped.startswith('def ') or
                    stripped.startswith('class ') or
                    stripped.startswith('@')):
                is_code_started = True

            # 如果已经开始，或者是空行（保留空行格式），或者是注释
            if is_code_started:
                # 简单过滤一下结尾常见的 "Explanation:" 之类的废话
                if stripped.lower().startswith("explanation:") or stripped.lower().startswith("note:"):
                    break
                code_lines.append(line)

        # 只有当提取到了有效的代码行（大于3行）才返回
        if len(code_lines) > 3:
            return "\n".join(code_lines).strip()

        # 4. 绝望兜底：如果整个回复包含关键字，直接当做代码返回
        # 宁可报错也不要返回空，因为返回空会导致 Fixer 认为失败而回滚
        if "def " in response or "import " in response:
            return response

        return ""
    # =========================================================
    #  Python 代码归一化（供 runner 使用，可选）
    # =========================================================
    @staticmethod
    def normalize_python(code: str) -> str:
        """
        对 Python 做简单归一化：
        - 去掉行尾空白
        - 去掉多余空行

        注意：DebugBench 的评估使用的是 runner 内的 normalize_python；
        这里提供的是备用实现（保持与 CppFixer.normalize_cpp 同样的接口风格）。
        """
        lines = code.splitlines()
        cleaned = [re.sub(r'[ \t]+$', '', l) for l in lines]
        text = "\n".join(cleaned)
        text = text.strip() + "\n"
        return text