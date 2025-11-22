"""
VerifierAgent - 多语言代码验证Agent（集成LLM动态运行时检测）
"""

import sys
import os
import math
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent
from utils.language_detector import Language
from verifiers.verifier_factory import VerifierFactory
from analyzers.scanner_factory import ScannerFactory

# 🔥 新增：尝试导入 LLM 动态测试模块
try:
    from analyzers.llm_dynamic_tester import run_dynamic_tests
except ImportError:
    run_dynamic_tests = None


class VerifierAgent(BaseAgent):
    """多语言代码验证Agent"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("VerifierAgent", config or {})
        self.verifiers = {}

    # ---------------------------------------------------------
    # 感知阶段
    # ---------------------------------------------------------
    def perceive(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        fix_results = input_data.get("fix_results", {})
        fixed_files = fix_results.get("fixed_files", [])
        original_files = input_data.get("original_files", [])
        original_analysis = input_data.get("original_analysis", {})
        test_cases = input_data.get("test_cases", [])
        attempt = input_data.get("attempt", 0)  # 🔥 新增：接收 attempt
        self.log(f"📊 收到修复结果：{len(fixed_files)} 个文件待验证")

        return {
            "fix_results": fix_results,
            "fixed_files": fixed_files,
            "original_files": original_files,
            "original_analysis": original_analysis,
            "test_cases": test_cases,
            "attempt": attempt  # 🔥 传递 attempt
        }

        # 决策阶段 (已修改：传递 original_files)
        # ---------------------------------------------------------
    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
            fixed_files = perception.get("fixed_files", [])
            test_cases = perception.get("test_cases", [])
            # 🔥 获取 original_files
            original_files = perception.get("original_files", [])
            attempt = perception.get("attempt", 0)  # 🔥 接收 attempt
            strategy = {
                "verification_plans": [],
                "enable_rescan": False,  # 🚫 禁用二次扫描
                "enable_tests": bool(test_cases),
                # 🔥 传递给 execute
                "original_files": original_files,
                "attempt": attempt  # 🔥 传递 attempt
            }

            files_by_language = {}
            for file in fixed_files:
                lang = file.get("language", "unknown")
                files_by_language.setdefault(lang, []).append(file)

            for lang_name, files in files_by_language.items():
                strategy["verification_plans"].append({
                    "language": lang_name,
                    "files": files,
                    "file_count": len(files)
                })

            self.log(f"\n决策：制定了 {len(strategy['verification_plans'])} 个验证计划")
            self.log(f"   - 功能测试: {'启用' if strategy['enable_tests'] else '禁用'}")

            return strategy

        # ---------------------------------------------------------
        # 执行阶段 (已修改：合并文件以构建完整测试环境)
        # ---------------------------------------------------------
    def execute(self, decision: Dict[str, Any]) -> Dict[str, Any]:
            verification_plans = decision.get("verification_plans", [])
            test_cases = decision.get("test_cases", [])
            # 🔥 获取 original_files
            all_original_files = decision.get("original_files", [])

            all_results = {
                "by_language": {},
                "verified_files": [],
                # 🔥 新增字段：用于 Orchestrator 判断是否需要回滚
                "dynamic_report": None,
                "has_dynamic_issues": False,
                "summary": {
                    "total_files": 0,
                    "compile_success": 0,
                    "test_passed": 0,
                    "total_original_issues": 0,
                    "total_fixed_issues": 0,
                    "total_new_issues": 0,
                    "dynamic_issues_count": 0  # 🔥 新增统计
                }
            }

            # 收集所有修复后的文件内容，用于后续统一进行动态测试
            all_fixed_files_content = []

            # 1. 执行常规验证（编译 + 静态复扫）
            for plan in verification_plans:
                lang_name = plan["language"]
                files = plan["files"]
                self.log(f"\n{'=' * 60}")
                self.log(f"✅ 验证 {lang_name.upper()} 修复结果，共 {len(files)} 个文件")

                lang = Language.from_string(lang_name)
                verifier = VerifierFactory.create_verifier(lang)
                verifier.allow_rescan = False
                scanner = ScannerFactory.create_scanner([], lang)

                # 将文件加入列表，准备做动态测试
                all_fixed_files_content.extend(files)

                for fixed_file in files:
                    filename = fixed_file.get("file")
                    self.log(f"\n   📄 验证文件: {filename}")

                    # 从 FixerAgent 报告读取
                    orig_count = fixed_file.get("original_issues_count", 0)
                    fixed_count = fixed_file.get("fixed_count", 0)
                    remaining_count = max(0, orig_count - fixed_count)
                    new_count = fixed_file.get("new_issues_count", 0)

                    # 通过 verifier 验证基本可执行性
                    verify_result = verifier.verify(
                        original_file=fixed_file,
                        fixed_file=fixed_file,
                        original_issues=fixed_file.get("original_issues", []),
                        test_cases=test_cases,
                        scanner=scanner
                    )

                    # 汇总统计
                    all_results["summary"]["total_files"] += 1
                    all_results["summary"]["total_original_issues"] += orig_count
                    all_results["summary"]["total_fixed_issues"] += fixed_count
                    all_results["summary"]["total_new_issues"] += new_count

                    if verify_result.compile_success:
                        all_results["summary"]["compile_success"] += 1
                    if verify_result.test_success:
                        all_results["summary"]["test_passed"] += 1

                    all_results["verified_files"].append({
                        "file": filename,
                        "language": lang_name,
                        "verification": verify_result.to_dict(),
                        "original_issues_count": orig_count,
                        "fixed_issues_count": fixed_count,
                        "remaining_issues_count": remaining_count,
                        "new_issues_count": new_count,
                        "fix_rate": (
                            100.0 * fixed_count / max(1, (orig_count + new_count))
                            if (orig_count + new_count) > 0 else 0.0
                        )
                    })

            # 2. 🔥🔥🔥 集成 LLM 动态运行时检测 (Dynamic Testing) 🔥🔥🔥
            if run_dynamic_tests:
                self.log(f"\n{'=' * 60}")
                self.log("🧪 执行 LLM 动态运行时检测 (Dynamic Testing)...")
                self.log("   正在生成针对性测试用例并执行...")

                try:
                    # 1. 建立全量文件映射
                    # 统一结构：Path -> {"content": str/None, "original_path": str/None}
                    project_files_map = {}

                    # 先处理原始文件
                    for f in all_original_files:
                        path = f.get("file")
                        content = f.get("content")
                        if path:
                            project_files_map[path] = {
                                "content": content,
                                "original_path": f.get("path")
                            }

                    # 用修复后的文件覆盖 (仅覆盖代码)
                    for f in all_fixed_files_content:
                        if f.get("success", False) and f.get("content"):
                            path = f.get("file")
                            if path:
                                # 🔥 修复：保持字典结构一致
                                project_files_map[path] = {
                                    "content": f.get("content"),
                                    "original_path": None  # 修复后的文件没有物理路径
                                }

                    # 3. 转换为 llm_dynamic_tester 需要的格式
                    dynamic_input_files = []
                    for path, data in project_files_map.items():
                        # 这里 data 一定是字典了
                        dynamic_input_files.append({
                            "file": path,
                            "content": data.get("content"),
                            "original_path": data.get("original_path"),
                            "original": ""
                        })

                    if dynamic_input_files:
                        self.log(f"   构建测试环境: 包含 {len(dynamic_input_files)} 个文件 (已合并原始文件与修复文件)")

                        # 执行动态测试
                        dynamic_report = run_dynamic_tests(
                            files=dynamic_input_files,
                            llm_config=self.config.get('llm_config', {}),
                            # 如果需要传递 extra_assets，可以在这里扩展
                            extra_assets=[]
                        )

                        all_results["dynamic_report"] = dynamic_report

                        # 分析结果
                        failed_tests = dynamic_report.get('failed', 0)
                        total_issues = dynamic_report.get('total_issues', 0)

                        if failed_tests > 0 or total_issues > 0:
                            all_results["has_dynamic_issues"] = True
                            all_results["summary"]["dynamic_issues_count"] = total_issues
                            self.log(f"  动态检测发现问题:")
                            self.log(f"   - 测试失败: {failed_tests} 个")
                            self.log(f"   - 运行时缺陷: {total_issues} 个")

                            # 打印部分详情
                            details = dynamic_report.get('details', [])
                            for d in details:
                                if not d.get('passed'):
                                    issues = d.get('issues_found', [])
                                    if issues:
                                        self.log(f"     🔴 {d.get('test_name')}: {issues[0]}")
                        else:
                            self.log("✅ 动态检测全部通过：未发现运行时异常、死锁或资源泄漏。")
                    else:
                        self.log("⚠️ 没有有效的文件内容进行动态测试。")

                except Exception as e:
                    self.log(f"⚠️ 动态检测执行过程中发生错误: {e}")
                    import traceback
                    traceback.print_exc()

            # ---------------------------------------------------------
            # ✅ 修复率计算（从 FixerAgent 数据汇总）
            # ---------------------------------------------------------
            s = all_results["summary"]
            total_files = s["total_files"]
            orig_total = s["total_original_issues"]
            fixed_total = s["total_fixed_issues"]
            new_total = s["total_new_issues"]
            compile_rate = s["compile_success"] / max(1, total_files)
            test_rate = s["test_passed"] / max(1, total_files)

            # ① 传统修复率
            trad_rate = 100 * fixed_total / max(1, (orig_total + new_total))
            # ② 动态修复率（编译 + 测试）
            dyn_rate = 100 * 0.5 * (compile_rate + test_rate)
            # ③ 综合修复率
            total_rate = 0.6 * trad_rate + 0.4 * dyn_rate

            # ④ 加权修复率（轻度惩罚）
            if total_files > 0:
                weights = []
                for vf in all_results["verified_files"]:
                    r = vf["fix_rate"] / 100
                    orig = vf["original_issues_count"]
                    rem = vf["remaining_issues_count"]
                    penalty = math.exp(-1.2 * (rem / (orig + 1)))
                    weights.append(r * penalty)
                weighted_rate = 100 * (sum(weights) / len(weights))
            else:
                weighted_rate = 0.0

            s.update({
                "traditional_fix_rate": trad_rate,
                "dynamic_fix_rate": dyn_rate,
                "total_fix_rate": total_rate,
                "weighted_fix_rate": weighted_rate
            })

            # ---------------------------------------------------------
            # ✅ 打印结果汇总 (实现条件输出)
            # ---------------------------------------------------------

            # 🔥 只有在 Round 0 (初始验证) 时才输出详细修复率统计
            if decision.get("attempt", 0) == 0:
                self.log(f"\n{'=' * 60}")
                self.log(f"📊 总体验证统计：")
                self.log(f"   - 文件总数: {total_files}")
                self.log(f"   - 原始问题: {orig_total}")
                self.log(f"   - 修复问题: {fixed_total}")
                self.log(f"   - 新增问题: {new_total}")
                self.log(f"   - 编译成功率: {compile_rate * 100:.2f}%")
                if s.get("dynamic_issues_count", 0) > 0:
                    self.log(f"   - ⚠️ 动态运行时缺陷: {s['dynamic_issues_count']} 个")

                # 🔥 Round 0 依然输出修复率
                self.log(f"   - ✅ 传统修复率: {trad_rate:.2f}%")
                self.log(f"   - 🧠 动态修复率: {dyn_rate:.2f}%")
                self.log(f"   - 🏁 综合修复率: {total_rate:.2f}%")

            # 🔥 即使不是 Round 0，也要输出动态检测结果（如果有的话）
            elif s.get("dynamic_issues_count", 0) > 0:
                self.log(f"\n{'=' * 60}")
                self.log(f"⚠️ 动态验证结果（Round {decision.get('attempt', 0)}）：")
                self.log(f"   - 编译成功率: {compile_rate * 100:.2f}%")
                self.log(f"   - ⚠️ 遗留动态缺陷: {s['dynamic_issues_count']} 个")

            return all_results