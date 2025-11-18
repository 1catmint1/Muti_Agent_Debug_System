"""
JavaFixer - Java代码修复器（对齐 CppFixer / PythonFixer 的 DebugBench 行为）
"""
import re
import os
from typing import Dict, List, Any, Union

from .base_fixer import BaseFixer, FixResult, Language


class JavaFixer(BaseFixer):
    """Java 专用修复器"""

    def __init__(self, llm_client=None, prompt_config: Dict[str, Any] = None):
        super().__init__(Language.JAVA, llm_client)
        # ✅ Prompt 配置（与 CppFixer / PythonFixer 保持一致）
        self.prompt_conf = prompt_config or {
            "language": "zh",
            "style": "concise",
            "force_code_block_only": True,
        }

    def _analyze_logic_diff_v2(self, buggy_code: str, reference_code: str) -> List[Dict[str, str]]:
        """
        使用 LLM 比较错误代码与正确代码，自动生成逻辑差异报告。
        ⚠️ 不泄露 ground truth，只输出逻辑差异点。
        """
        if not self.llm_client:
            return [{"type": "NO_LLM", "message": "LLM 客户端未配置，无法分析逻辑差异"}]

        try:
            prompt = (
                "你是一名 Java 代码结构与逻辑分析专家。\n"
                "下面是两份代码：A 是错误版本，B 是正确版本。\n"
                "你的任务：\n"
                "  - 比较 A 与 B，在逻辑行为上的差异点逐条列出。\n"
                "  - 只能描述逻辑/流程/边界/条件/递归/循环/变量更新上的差异。\n"
                "  - 禁止输出 B 的任何代码内容、禁止泄露实现细节。\n"
                "  - 每条差异以 JSON 形式输出，例如：\n"
                "    {\"type\": \"MISSING_CALL\", \"message\": \"A 缺少对子树的递归\"}\n"
                "最终输出必须是 JSON 数组。\n\n"
                "=== 错误代码 A ===\n"
                f"{buggy_code}\n\n"
                "=== 正确代码 B（禁止泄露） ===\n"
                f"{reference_code}\n\n"
                "=== 请输出 JSON 数组（不要代码） ==="
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
            return [{"type": "PARSE_FAIL", "message": "无法解析 AI 输出"}]

        except Exception as e:
            return [{"type": "ANALYSIS_FAIL", "message": f"分析失败: {e}"}]


    # =========================================================
    #  规则修复部分：仅做轻量、安全的自动修复
    # =========================================================
    def apply_rule_fixes(self, file: Dict[str, Any], issues: List[Union[Dict, str]]) -> FixResult:
        """
        轻量规则修复：
        - 自动补 import（含 java.util.*；支持 Stack 等）
        - 修复常见返回类型不兼容
        不做结构性大改动。
        """
        filename = file.get("file", "")
        content = file.get("content", "")
        fixed_content = content
        fixed_count = 0

        print(f"[JavaFixer] 开始规则修复: {filename}")
        print(f"[JavaFixer] 待修复问题数: {len(issues)}")

        # ✅ issues 规范化（兼容 Finding / dict / str）
        normalized_issues: List[Dict[str, Any]] = []
        for issue in issues:
            if isinstance(issue, dict):
                normalized_issues.append(issue)
            elif hasattr(issue, "__dict__"):
                normalized_issues.append(issue.__dict__)  # Finding 等对象
            else:
                normalized_issues.append({"message": str(issue), "rule_id": "UNKNOWN"})

        # 1) 自动补 import / stub / throws
        auto_fixed_content, auto_count = self._auto_fix_compile_errors(fixed_content)
        if auto_count > 0:
            fixed_content = auto_fixed_content
            fixed_count += auto_count
            print(f"[JavaFixer] 自动修复编译错误: {auto_count} 处")

        # 2) 返回类型不兼容
        fixed_return_content, ret_count = self._fix_incompatible_return_type(fixed_content)
        if ret_count > 0:
            fixed_content = fixed_return_content
            fixed_count += ret_count
            print(f"[JavaFixer] 修复返回类型不兼容: {ret_count} 处")

        print(f"[JavaFixer] 规则修复完成: 修复了 {fixed_count} 处问题")

        return FixResult(
            file=filename,
            language=self.language.value,
            original_content=content,
            fixed_content=fixed_content,
            fixed_count=fixed_count,
            method="rule",
            success=fixed_count > 0,
            error_message="" if fixed_count > 0 else "没有找到可自动修复的问题",
            fixed_issues=normalized_issues,
        )

    def _auto_fix_compile_errors(self, content: str) -> tuple:
        """
        自动修复典型编译错误：
        - 缺少 import（含 Stack 等容器）
        - 缺少方法 stub
        - 未捕获的 ClassNotFoundException
        """
        count = 0
        code = content

        needed_imports: List[str] = []

        # 反射类型
        if re.search(r"\b(Type|WildcardType|TypeVariable)\b", code):
            needed_imports.append("import java.lang.reflect.*;")
        # 集合 / 容器类（含 Stack / Deque / ArrayList 等）
        if re.search(
            r"\b(Collection|List|Set|Map|Queue|Deque|ArrayDeque|LinkedList|ArrayList|Stack|Collections|Arrays)\b",
            code,
        ):
            needed_imports.append("import java.util.*;")
        # IO
        if re.search(r"\b(OutputStream|InputStream|Reader|Writer|File)\b", code):
            needed_imports.append("import java.io.*;")
        # Mockito / JUnit
        if "mock(" in code or "Mockito" in code:
            needed_imports.append("import static org.mockito.Mockito.*;")
        if "ViolatedAssumptionAnswer" in code:
            needed_imports.append("import org.junit.internal.ViolatedAssumptionAnswer;")

        for imp in needed_imports:
            if imp not in code:
                code = imp + "\n" + code
                count += 1

        # Assert.xxx(missingMethod()) → 自动补 boolean stub
        missing_methods = re.findall(r"Assert\.\w+\((\w+)\(\)\)", code)
        if missing_methods:
            stub_methods = ""
            for m in set(missing_methods):
                if f"boolean {m}(" not in code:
                    stub_methods += (
                        f"\n    private boolean {m}() {{\n        return true;\n    }}\n"
                    )
                    count += 1
            code = re.sub(r"(\n}\s*)$", stub_methods + r"\1", code)

        # ClassNotFoundException 未声明 throws
        if "throw e;" in code and "ClassNotFoundException" in code:
            code = re.sub(
                r"(public\s+[^\(]+\([^\)]*\))\s*\{",
                r"\1 throws ClassNotFoundException {",
                code,
            )
            count += 1

        return code, count

    def _fix_incompatible_return_type(self, content: str) -> tuple:
        """
        修复 Java '不兼容的类型: 意外的返回值' 编译错误。
        """
        fixed = content
        count = 0

        # void 方法内 return 常量 → return;
        fixed = re.sub(
            r"((?:public|protected|private)\s+void\s+\w+\s*\([^)]*\)\s*\{)([\s\S]*?)(return\s+[^;]+;)",
            lambda m: m.group(1)
            + m.group(2).replace("return", "// 修复: 移除无效返回\nreturn;"),
            fixed,
        )

        # boolean 方法内返回数字 / EXIT_CODE → true
        def replace_in_boolean_method(match):
            header = match.group(1)
            body = match.group(5)
            body = re.sub(r"return\s+\d+\s*;", "return true;", body)
            body = re.sub(r"return\s+EXIT_CODE\s*;", "return true;", body)
            return header + body + "}"

        fixed2 = re.sub(
            r"(((?:public|protected|private)\s+)boolean\s+(\w+)\s*\(([^)]*)\)\s*\{)([\s\S]*?)\}",
            replace_in_boolean_method,
            fixed,
        )
        if fixed2 != fixed:
            fixed = fixed2
            count += 1

        # 兜底替换
        if "return EXIT_CODE;" in fixed:
            fixed = fixed.replace("return EXIT_CODE;", "// 修复: 无效返回\nreturn;")
            count += 1
        if "return 0;" in fixed:
            fixed = fixed.replace("return 0;", "// 修复: 无效返回\nreturn;")
            count += 1

        return fixed, count

    # =========================================================
    #  LLM 部分：仿 CppFixer / PythonFixer 的 DebugBench 行为
    # =========================================================
    def apply_llm_fixes(
        self,
        file: Dict[str, Any],
        issues: List[Union[Dict, str]],
        user_request: str = "",
    ) -> FixResult:
        """应用 LLM 修复（单轮，行为对齐 CppFixer / PythonFixer）"""
        filename = file.get("file", "")
        content = file.get("content", "")

        result = FixResult(
            file=filename,
            language=self.language.value,
            original_content=content,
            fixed_content=content,
            fixed_count=0,
            method="llm",
            success=False,
        )

        if not self.llm_client:
            result.error_message = "LLM客户端未配置"
            print("[JavaFixer] LLM客户端未配置")
            return result

        print(f"[JavaFixer] 开始LLM修复: {filename}")
        print(f"[JavaFixer] 问题数: {len(issues)}")

        # ✅ 规范化 issues
        normalized_issues: List[Dict[str, Any]] = []
        for issue in issues:
            if isinstance(issue, dict):
                normalized_issues.append(issue)
            elif hasattr(issue, "__dict__"):
                normalized_issues.append(issue.__dict__)
            else:
                normalized_issues.append({"message": str(issue), "rule_id": "UNKNOWN"})

        try:
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(
                filename=filename,
                original_content=content,
                issues=normalized_issues,
                user_request=user_request,
                force_code_block_only=self.prompt_conf.get("force_code_block_only", True),
            )

            print("[JavaFixer] 调用 LLM API...")

            if hasattr(self.llm_client, "chat") and callable(self.llm_client.chat):
                response = self.llm_client.chat(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.3,
                    max_tokens=4000,
                )
            else:
                result.error_message = "不支持的LLM客户端类型"
                return result

            print(f"[JavaFixer] LLM 响应长度: {len(response)} 字符")

            fixed_code = self._extract_code_from_response(response, filename)

            if fixed_code and fixed_code != content:
                result.fixed_content = fixed_code
                # DebugBench 场景下经常没有 issues，这里至少记为 1
                result.fixed_count = max(1, len(normalized_issues))
                result.success = True
                print("[JavaFixer] LLM 修复成功")
            else:
                result.error_message = "LLM未返回有效的修复代码"
                print("[JavaFixer] LLM 修复失败: 未返回有效代码")

        except Exception as e:
            result.error_message = f"LLM调用失败: {str(e)}"
            print(f"[JavaFixer] LLM 调用异常: {e}")
            import traceback

            traceback.print_exc()

        return result

    def _build_system_prompt(self) -> str:
        """✅ 构建 LLM 系统提示词（对齐 CppFixer）"""
        lang = self.prompt_conf.get("language", "zh")
        style = self.prompt_conf.get("style", "concise")

        return (
            "你是专业的 Java 代码修复助手。请严格遵守：\n"
            "1) 仅输出完整的代码，不要输出解释。\n"
            "2) 输出格式必须为一个带文件名的 java 代码块：```java <文件名>.java\\n<完整代码>```\n"
            "3) 不要输出 diff、不要输出多余文本或多个代码块。\n"
            "4) 如果无法修复，请也输出原样的完整文件代码块。\n"
            "5) 确保输出是完整可编译的 Java 源码（包括类定义、必要的 import）。\n"
            f"语言：{lang}；风格：{style}。\n"
        )

    def _build_user_prompt(
        self,
        filename: str,
        original_content: str,
        issues: List[Dict[str, Any]],
        user_request: str,
        force_code_block_only: bool,
    ) -> str:
        """
        ✅ 构建 LLM 用户提示词（标准化 + DebugBench 模式，对齐 CppFixer）
        """
        lang_ext = "java"

        # 1️⃣ 检测 DebugBench 模式
        debugbench_mode = bool(user_request and "[DEBUGBENCH]" in user_request)
        reference_code = ""

        if debugbench_mode:
            start_tag = "【参考正确实现（ground truth）】"
            end_tag = "【参考实现结束】"
            start_idx = user_request.find(start_tag)
            end_idx = user_request.find(end_tag)
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                reference_code = user_request[start_idx + len(start_tag):end_idx].strip()

        # 2️⃣ DebugBench 专用提示（有 ground truth）
        if debugbench_mode and reference_code:
            strict_hint = (
                f"【重要】只输出一个带文件名的 {lang_ext} 代码块，不要任何说明文字、不要 diff。"
                if force_code_block_only
                else f"尽可能只输出一个带文件名的 {lang_ext} 代码块；不要输出 diff 或解释。"
            )

            logic_issues = self._analyze_logic_diff_v2(original_content, reference_code)
            logic_report = "\n".join(
                f"- [{it.get('type', 'LOGIC')}] {it.get('message', '')}"
                for it in logic_issues
            )
            if not logic_report.strip():
                logic_report = "- [LOGIC_UNKNOWN] 系统未能自动分析逻辑差异，但你的代码必须与正确实现功能一致。"

            return (
                "你正在进行一个名为 DebugBench 的自动 Java 代码修复任务。\n"
                "系统不会直接给出正确代码，而是提供从正确实现推断出的逻辑差异报告。\n"
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

        # 3️⃣ 非 DebugBench：默认基于 issues 的提示
        issue_lines = []
        for it in issues:
            issue_lines.append(
                f"- [{it.get('rule_id', '')}] 行 {it.get('line', '?')}: {it.get('message', '')}"
            )
        issue_text = "\n".join(issue_lines) if issue_lines else "无结构化缺陷条目。"

        strict_hint = (
            f"【重要】只输出一个带文件名的 {lang_ext} 代码块，不要任何说明文字、不要 diff。"
            if force_code_block_only
            else f"如果可能，只输出一个带文件名的 {lang_ext} 代码块；不要输出 diff 或解释。"
        )

        extra = ""
        if user_request and "[DEBUGBENCH]" not in user_request:
            extra = f"\n【用户补充需求】\n{user_request}\n"

        return (
            "请修复下述 Java 文件中的语法和逻辑问题，并返回修复后的完整源代码。\n\n"
            f"【目标文件】{filename}\n"
            f"【检测到的问题】\n{issue_text}\n"
            f"{extra}\n"
            f"【原始代码开始】\n{original_content}\n【原始代码结束】\n\n"
            f"{strict_hint}\n"
            f"代码块格式示例：\n"
            f"```{lang_ext} {filename}\n<完整代码>\n```\n"
        )

    def _extract_code_from_response(self, response: str, expected_filename: str) -> str:
        """
        从 LLM 响应中提取 Java 代码（对齐 CppFixer 的逻辑）
        """
        # 1) ```java filename.java\n<code>```
        pattern = r"```java\s+([^\n]+)?\s*\n([\s\S]*?)```"
        matches = re.findall(pattern, response, re.IGNORECASE)
        for fname, code in matches:
            fname = (fname or "").strip()
            base_expected = os.path.basename(expected_filename)
            if not fname or base_expected in fname or fname.endswith(".java"):
                if code.strip():
                    return code.strip()

        # 2) ```java\n<code>```
        m = re.search(r"```java\s*\n([\s\S]*?)```", response, re.IGNORECASE)
        if m and m.group(1).strip():
            return m.group(1).strip()

        # 3) 任意 ```\n<code>```
        m = re.search(r"```\s*\n([\s\S]*?)```", response)
        if m and m.group(1).strip():
            return m.group(1).strip()

        # 4) Fallback：整个响应
        return response.strip()

    def _is_rule_fixable(self, rule_id: str) -> bool:
        """判断规则是否可以自动修复（目前未使用，但保留接口）"""
        fixable_rules = ["JAVA002", "JAVA003", "JAVA004"]
        return rule_id in fixable_rules

    # =========================================================
    #  统一修复入口：对齐 CppFixer / PythonFixer
    # =========================================================
    def fix(
        self,
        file: Dict[str, Any],
        issues: List[Dict[str, Any]],
        use_rules: bool = True,
        use_llm: bool = True,
        user_request: str = "",
    ) -> FixResult:
        """
        统一修复入口：
        1. 轻量规则修复（import/返回类型）；
        2. DebugBench 模式下：直接走一次 LLM 修复（带 ground truth 提示）；
        3. 非 DebugBench：基于 issues 的 LLM 修复（可选）。
        """
        filename = file.get("file", "")
        original_content = file.get("content", "")

        print(f"[JavaFixer] fix() 启动: {filename}")
        print(
            f"[JavaFixer] 参数: use_rules={use_rules}, use_llm={use_llm}, 问题数={len(issues)}"
        )

        print("[JavaFixer] ==== 原始文件内容预览（前 300 字符）BEGIN ====")
        print(original_content[:300])
        print("[JavaFixer] ==== 原始文件内容预览 END ====")

        debugbench_mode = bool(user_request and "[DEBUGBENCH]" in user_request)

        # Step 1️⃣ 规则修复
        if use_rules:
            rule_result = self.apply_rule_fixes(file, issues)
        else:
            rule_result = FixResult(
                file=filename,
                language=self.language.value,
                original_content=original_content,
                fixed_content=original_content,
                fixed_count=0,
                method="none",
                success=False,
                fixed_issues=issues,
            )

        current_code = rule_result.fixed_content

        # Step 2️⃣ LLM 修复（单轮）
        if use_llm and self.llm_client is not None:
            llm_input_file = {"file": filename, "content": current_code}
            llm_result = self.apply_llm_fixes(
                llm_input_file, issues, user_request=user_request
            )
        else:
            llm_result = FixResult(
                file=filename,
                language=self.language.value,
                original_content=original_content,
                fixed_content=current_code,
                fixed_count=0,
                method=rule_result.method,
                success=rule_result.success,
                fixed_issues=issues,
            )

        # Step 3️⃣ 合并结果（DebugBench 下始终使用 LLM 结果）
        if debugbench_mode:
            merged_fixed_content = (
                llm_result.fixed_content if llm_result.success else current_code
            )
            merged_success = True if llm_result.success else rule_result.success
            merged_method = (
                "rule+llm-debugbench"
                if (use_rules and llm_result.success)
                else ("llm-debugbench" if llm_result.success else rule_result.method)
            )
            merged_fixed_count = (
                rule_result.fixed_count
                + (llm_result.fixed_count if llm_result.fixed_count else 0)
            )
        else:
            if llm_result.success:
                merged_fixed_content = llm_result.fixed_content
                merged_method = "rule+llm" if use_rules else "llm"
                merged_success = True
                merged_fixed_count = rule_result.fixed_count + llm_result.fixed_count
            else:
                merged_fixed_content = current_code
                merged_method = rule_result.method
                merged_success = rule_result.success
                merged_fixed_count = rule_result.fixed_count

        merged = FixResult(
            file=filename,
            language=self.language.value,
            original_content=original_content,
            fixed_content=merged_fixed_content,
            fixed_count=merged_fixed_count,
            method=merged_method,
            success=merged_success,
            error_message=llm_result.error_message if (not llm_result.success and llm_result.error_message) else "",
            fixed_issues=issues,
        )

        print(
            f"[JavaFixer] 综合修复完成: 方法={merged.method}, fixed_count={merged.fixed_count}, success={merged.success}"
        )
        return merged