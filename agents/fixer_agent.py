# agents/fixer_agent.py
"""
FixerAgent - 多语言代码修复Agent
"""
import sys
import os
from typing import Dict, Any, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent
from utils.language_detector import Language, LanguageDetector
from fixers.fixer_factory import FixerFactory


class FixerAgent(BaseAgent):
    """多语言代码修复Agent"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("FixerAgent", config or {})
        self.llm_client = config.get("llm_client") if config else None
        self.fixers = {}

    def perceive(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """感知阶段：接收分析结果或动态反馈"""
        analysis = input_data.get("analysis", {})
        files = input_data.get("files", [])
        user_request = input_data.get("user_request", "")

        # 🔥 新增：接收来自 VerifierAgent 的动态检测反馈
        dynamic_feedback = input_data.get("dynamic_feedback", None)

        by_language = analysis.get("by_language", {})

        # 只有在没有动态反馈时才打印常规日志，避免刷屏
        if not dynamic_feedback:
            self.log(f"📊 收到分析结果：涉及 {len(by_language)} 种语言")
            for lang, lang_analysis in by_language.items():
                # 安全地获取 total
                total = lang_analysis.get("total", 0) if isinstance(lang_analysis, dict) else 0
                self.log(f"   - {lang.upper()}: {total} 个问题待修复")
        else:
            self.log(f"🔄 收到动态检测反馈 (Dynamic Feedback)，准备进行针对性修复...")

        # 检查 LLM 配置
        use_llm = self.config.get("use_llm", True) and self.llm_client is not None

        return {
            "analysis": analysis,
            "files": files,
            "by_language": by_language,
            "user_request": user_request,
            "dynamic_feedback": dynamic_feedback,  # 传递给决策层
            "use_rules": self.config.get("use_rules", True),
            "use_llm": use_llm
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        决策阶段：确定修复策略
        优先处理动态反馈，否则处理常规静态分析结果
        """
        by_language = perception.get("by_language", {}) or {}
        use_rules = perception.get("use_rules", True)
        use_llm = perception.get("use_llm", False)
        files = perception.get("files", []) or []
        user_request = perception.get("user_request", "") or ""
        dynamic_feedback = perception.get("dynamic_feedback")

        # DebugBench 模式：通过 user_request 标记
        debugbench_mode = "[DEBUGBENCH" in user_request
        # 兜底配置
        force_llm_cfg = self.config.get("force_llm_on_empty", False)

        strategy = {
            "repair_plans": [],
            "use_rules": use_rules,
            "use_llm": use_llm,
            "files": files,
            "user_request": user_request,
        }

        # ============================================================
        # 🔥 优先路径：处理动态检测反馈 (Dynamic Feedback)
        # ============================================================
        if dynamic_feedback:
            self.log("   ⚙️ [高优先级] 正在根据动态检测报告生成修复计划...")

            # 解析 llm_dynamic_tester 的报告
            details = dynamic_feedback.get('details', [])
            issues_by_file = {}

            for test_result in details:
                if not test_result.get('passed', False):
                    test_name = test_result.get('test_name', '')
                    issues = test_result.get('issues_found', [])
                    error_msg = test_result.get('error', '')

                    # 构造错误描述
                    full_msg = f"[Dynamic Runtime Error] Test '{test_name}' Failed."
                    if issues:
                        full_msg += f"\nIssues Found: {'; '.join(issues)}"
                    if error_msg:
                        full_msg += f"\nSystem Error: {error_msg}"

                    # 尝试将错误关联到文件
                    # llm_dynamic_tester 生成的测试名通常是 test_{category}_{filename}
                    # 这是一个简单的启发式匹配
                    target_file = None
                    for f in files:
                        fname = f.get('file', '')
                        base_name = os.path.basename(fname)
                        # 简单去扩展名匹配
                        name_no_ext = os.path.splitext(base_name)[0]
                        if name_no_ext in test_name:
                            target_file = fname
                            break

                    # 如果没匹配到，关联到第一个同类语言文件，或者所有文件
                    if not target_file and files:
                        # 默认关联到第一个 Python 文件（因为目前动态检测主要是 Python）
                        for f in files:
                            if f.get('file', '').endswith('.py'):
                                target_file = f.get('file')
                                break

                    if target_file:
                        if target_file not in issues_by_file:
                            issues_by_file[target_file] = []

                        issues_by_file[target_file].append({
                            "rule_id": "DYNAMIC_RUNTIME_ERROR",
                            "message": full_msg,
                            "severity": "HIGH",  # 动态错误通常是严重的
                            "file": target_file,
                            "line": 0  # 全局问题，无法定位具体行
                        })

            if issues_by_file:
                plan = {
                    "language": "python",  # 假设动态测试主要是 Python
                    "files_to_fix": [],
                    "total_issues": sum(len(v) for v in issues_by_file.values())
                }

                for fname, issues in issues_by_file.items():
                    plan["files_to_fix"].append({
                        "filename": fname,
                        "issues": issues,
                        "issue_count": len(issues)
                    })

                strategy["repair_plans"].append(plan)
                self.log(f"   ✅ 已生成动态修复计划，包含 {plan['total_issues']} 个运行时问题。")
                return strategy
            else:
                self.log("   ⚠️ 收到动态反馈但无法解析出具体文件的问题，回退到常规修复。")

        # ============================================================
        # 1️⃣ 正常路径：根据 Analyzer 提供的静态分析结果构造修复计划
        # ============================================================
        for lang_name, lang_analysis in by_language.items():
            # ... (保持原有的正常路径逻辑不变)
            if not isinstance(lang_analysis, dict):
                continue

            issues_by_file = lang_analysis.get("issues_by_file", {}) or {}
            total_issues = lang_analysis.get("total", 0) or 0

            # ... (省略部分原逻辑：如果 AnalyzerAgent 没生成 issues_by_file，就尝试从 builtin/external 提取)

            # 如果仍然没有 issue，先不为该语言创建 plan
            if not issues_by_file:
                continue

            repair_plan = {
                "language": lang_name,
                "files_to_fix": [],
                "total_issues": total_issues
            }

            for filename, issues in issues_by_file.items():
                if not isinstance(issues, list):
                    issues = [issues]

                repair_plan["files_to_fix"].append({
                    "filename": filename,
                    "issues": issues,
                    "issue_count": len(issues)
                })

            strategy["repair_plans"].append(repair_plan)

        # ============================================================
        # 2️⃣ DebugBench 兜底逻辑
        # ============================================================
        if debugbench_mode and not strategy["repair_plans"]:
            self.log("   ⚙️ DebugBench 模式启用：无问题也强制修复")
            # ... (省略 DebugBench 详细生成虚拟 plan 的代码，逻辑同原版)

        # ============================================================
        # 3️⃣ 实际场景兜底逻辑 (Force LLM on Empty)
        # ============================================================
        # ... (省略兜底逻辑辅助函数)

        # 构造按语言分组的文件
        files_by_lang_for_fallback = {}
        for f in files:
            path = f.get("file", "") or ""
            lower = path.lower()
            if lower.endswith(".py"):
                lang = "python"
            elif lower.endswith(".java"):
                lang = "java"
            elif lower.endswith((".cpp", ".cc", ".c", ".h")):
                lang = "cpp"
            else:
                continue
            files_by_lang_for_fallback.setdefault(lang, []).append(f)

        planned_langs = {p["language"] for p in strategy["repair_plans"]}

        # ... (省略实际场景兜底的具体循环逻辑，逻辑同原版)

        # ============================================================
        # 4️⃣ 日志输出
        # ============================================================
        self.log(f"决策：制定了 {len(strategy['repair_plans'])} 个修复计划")
        return strategy

    def execute(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """执行阶段：对每种语言执行修复"""
        repair_plans = decision.get("repair_plans", [])
        use_rules = decision.get("use_rules", True)
        use_llm = decision.get("use_llm", False)
        user_request = decision.get("user_request", "")

        all_results = {
            "by_language": {},
            "fixed_files": [],
            "summary": {
                "total_files": 0,
                "successfully_fixed": 0,
                "failed": 0,
                "total_fixes": 0
            }
        }

        # 获取原始文件映射
        files = decision.get("files", [])
        file_map = {f.get("file"): f for f in files}

        print(f"\n🔥🔥🔥 [DEBUG] file_map 构建完成，共 {len(file_map)} 个文件")
        for k in list(file_map.keys())[:3]:
            print(f"🔥🔥🔥 [DEBUG] file_map key 示例: {k}")

        # 对每种语言执行修复
        for plan in repair_plans:
            lang_name = plan["language"]
            files_to_fix = plan["files_to_fix"]

            self.log(f"\n{'=' * 60}")
            self.log(f"🔧 开始修复 {lang_name.upper()} 代码...")
            self.log(f"   待修复文件数: {len(files_to_fix)}")

            try:
                # 获取语言枚举
                lang = Language.from_string(lang_name)

                # 创建修复器
                fixer = FixerFactory.create_fixer(lang, self.llm_client)

                lang_results = {
                    "language": lang_name,
                    "files": [],
                    "summary": {
                        "total": len(files_to_fix),
                        "success": 0,
                        "failed": 0
                    }
                }

                # 修复每个文件
                for file_info in files_to_fix:
                    filename = file_info["filename"]
                    issues = file_info["issues"]

                    self.log(f"\n   📄 修复文件: {filename}")
                    self.log(f"      问题数: {len(issues)}")

                    print(f"\n🔥🔥🔥 [DEBUG] 准备修复文件: {filename}")
                    print(f"🔥🔥🔥 [DEBUG] issues 数量: {len(issues)}")

                    # =========================================================
                    # 🔥 关键修复：超级增强的文件查找逻辑
                    # =========================================================
                    original_file = None
                    matched_key = None

                    # 策略 1: 精确匹配
                    if filename in file_map:
                        original_file = file_map[filename]
                        matched_key = filename
                        print(f"🔥🔥🔥 [DEBUG] ✅ 策略1成功：精确匹配 {filename}")

                    # 策略 2: 通过 basename 匹配
                    if not original_file:
                        basename_to_find = os.path.basename(filename)
                        print(f"🔥🔥🔥 [DEBUG] 策略2：尝试 basename 匹配 {basename_to_find}")

                        for full_path, file_obj in file_map.items():
                            if os.path.basename(full_path) == basename_to_find:
                                original_file = file_obj
                                matched_key = full_path
                                print(f"🔥🔥🔥 [DEBUG] ✅ 策略2成功：basename 匹配到 {full_path}")
                                break

                    # 策略 3: 路径包含关系匹配（双向，且标准化路径）
                    if not original_file:
                        print(f"🔥🔥🔥 [DEBUG] 策略3：尝试路径包含关系匹配")
                        norm_filename = filename.replace("\\", "/").lower()

                        for full_path, file_obj in file_map.items():
                            norm_full_path = full_path.replace("\\", "/").lower()

                            # 双向检查包含关系
                            if norm_filename in norm_full_path or norm_full_path in norm_filename:
                                original_file = file_obj
                                matched_key = full_path
                                print(f"🔥🔥🔥 [DEBUG] ✅ 策略3成功：路径包含匹配到 {full_path}")
                                break

                    # 策略 4: 最后兜底 - 如果只有一个文件且语言匹配，直接使用
                    if not original_file and len(file_map) == 1:
                        print(f"🔥🔥🔥 [DEBUG] 策略4：file_map 只有一个文件，直接使用")
                        matched_key = list(file_map.keys())[0]
                        original_file = file_map[matched_key]
                        print(f"🔥🔥🔥 [DEBUG] ✅ 策略4成功：使用唯一文件 {matched_key}")

                    if not original_file:
                        print(f"🔥🔥🔥 [DEBUG] ❌ 所有策略失败！无法找到文件")
                        self.log(f"      ⚠️ [严重] 未找到原始文件，跳过修复。")
                        self.log(f"         尝试查找的文件名: {filename}")
                        self.log(f"         file_map 中的可用键:")
                        for k in file_map.keys():
                            self.log(f"           - {k}")

                        lang_results["summary"]["failed"] += 1
                        all_results["summary"]["failed"] += 1

                        # ✅ 即使找不到文件，也添加一个错误记录
                        all_results["fixed_files"].append({
                            "file": filename,
                            "content": "",
                            "language": lang_name,
                            "original_content": "",
                            "fixed_count": 0,
                            "method": "none",
                            "status": "error",
                            "success": False,
                            "error_message": "未在 file_map 中找到对应的原始文件"
                        })
                        continue

                    # ✅ 找到文件后，使用 matched_key 作为最终的 filename
                    filename = matched_key
                    print(f"🔥🔥🔥 [DEBUG] 最终使用的 filename: {filename}")

                    try:
                        print(f"🔥🔥🔥 [DEBUG] 调用 fixer.fix() 开始")

                        # 执行修复
                        fix_result = fixer.fix(
                            original_file,
                            issues,
                            use_rules=use_rules,
                            use_llm=use_llm,
                            user_request=user_request
                        )

                        print(
                            f"🔥🔥🔥 [DEBUG] fixer.fix() 返回: success={fix_result.success}, method={fix_result.method}, fixed_count={fix_result.fixed_count}")

                        # 构建输出文件
                        fixed_file = {
                            "file": filename,
                            "content": fix_result.fixed_content if fix_result.success else original_file.get("content"),
                            "language": lang_name,
                            "original_content": original_file.get("content"),
                            "fixed_count": fix_result.fixed_count,
                            "method": fix_result.method,
                            "status": "fixed" if fix_result.success else "failed",
                            "success": fix_result.success,
                            "error_message": fix_result.error_message if not fix_result.success else "",
                            "original_issues": issues,
                            "original_issues_count": len(issues)
                        }

                        print(f"🔥🔥🔥 [DEBUG] 构建 fixed_file 完成，准备添加到 all_results['fixed_files']")

                        all_results["fixed_files"].append(fixed_file)
                        lang_results["files"].append(fix_result.to_dict())

                        print(f"🔥🔥🔥 [DEBUG] fixed_file 已添加，当前 fixed_files 数量: {len(all_results['fixed_files'])}")

                        # 更新统计和日志
                        if fix_result.success:
                            self.log(f"      ✅ 修复成功！ (方法: {fix_result.method}, 修复数: {fix_result.fixed_count})")
                            lang_results["summary"]["success"] += 1
                            all_results["summary"]["successfully_fixed"] += 1
                            all_results["summary"]["total_fixes"] += fix_result.fixed_count
                        else:
                            self.log(f"      ⚠️ 未修复: {fix_result.error_message or '未知错误'}")
                            lang_results["summary"]["failed"] += 1
                            all_results["summary"]["failed"] += 1

                    except Exception as e:
                        self.log(f"      ❌ 在文件修复过程中发生异常: {str(e)}")
                        import traceback
                        traceback.print_exc()

                        lang_results["summary"]["failed"] += 1
                        all_results["summary"]["failed"] += 1

                        all_results["fixed_files"].append({
                            "file": filename,
                            "content": original_file.get("content"),
                            "language": lang_name,
                            "original_content": original_file.get("content"),
                            "fixed_count": 0,
                            "method": "none",
                            "status": "error",
                            "success": False,
                            "error_message": str(e)
                        })

                all_results["by_language"][lang_name] = lang_results
                all_results["summary"]["total_files"] += len(files_to_fix)

                self.log(
                    f"\n   ✅ {lang_name.upper()} 修复完成: {lang_results['summary']['success']} 成功, {lang_results['summary']['failed']} 失败。")

            except Exception as e:
                self.log(f"   ❌ 在为语言 {lang_name.upper()} 设置修复器时发生严重错误: {str(e)}")
                import traceback
                traceback.print_exc()

        self.log(f"\n{'=' * 60}")
        self.log(f"📊 总体修复统计：")
        self.log(f"   - 处理文件: {all_results['summary']['total_files']} 个")
        self.log(f"   - 成功修复: {all_results['summary']['successfully_fixed']} 个")
        self.log(f"   - 修复失败: {all_results['summary']['failed']} 个")
        self.log(f"   - 总修复数: {all_results['summary']['total_fixes']} 处")
        self.log(f"   - fixed_files 列表总数: {len(all_results['fixed_files'])} 个")

        print(f"\n🔥🔥🔥 [DEBUG] execute() 完成，最终 fixed_files 数量: {len(all_results['fixed_files'])}")

        return all_results