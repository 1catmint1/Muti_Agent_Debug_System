"""
VerifierAgent - 多语言代码验证Agent（无复扫版 + 基于Fixer报告的全局修复率计算）
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

        self.log(f"📊 收到修复结果：{len(fixed_files)} 个文件待验证")

        return {
            "fix_results": fix_results,
            "fixed_files": fixed_files,
            "original_files": original_files,
            "original_analysis": original_analysis,
            "test_cases": test_cases
        }

    # ---------------------------------------------------------
    # 决策阶段
    # ---------------------------------------------------------
    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        fixed_files = perception.get("fixed_files", [])
        test_cases = perception.get("test_cases", [])

        strategy = {
            "verification_plans": [],
            "enable_rescan": False,  # 🚫 禁用二次扫描
            "enable_tests": bool(test_cases)
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
    # 执行阶段
    # ---------------------------------------------------------
    def execute(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        verification_plans = decision.get("verification_plans", [])
        test_cases = decision.get("test_cases", [])

        all_results = {
            "by_language": {},
            "verified_files": [],
            "summary": {
                "total_files": 0,
                "compile_success": 0,
                "test_passed": 0,
                "total_original_issues": 0,
                "total_fixed_issues": 0,
                "total_new_issues": 0
            }
        }

        for plan in verification_plans:
            lang_name = plan["language"]
            files = plan["files"]
            self.log(f"\n{'=' * 60}")
            self.log(f"✅ 验证 {lang_name.upper()} 修复结果，共 {len(files)} 个文件")

            lang = Language.from_string(lang_name)
            verifier = VerifierFactory.create_verifier(lang)
            verifier.allow_rescan = False
            scanner = ScannerFactory.create_scanner([], lang)

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
        # ✅ 打印结果汇总
        # ---------------------------------------------------------
        self.log(f"\n{'=' * 60}")
        self.log(f"📊 总体验证统计：")
        self.log(f"   - 文件总数: {total_files}")
        self.log(f"   - 原始问题: {orig_total}")
        self.log(f"   - 修复问题: {fixed_total}")
        self.log(f"   - 新增问题: {new_total}")
        self.log(f"   - 编译成功率: {compile_rate*100:.2f}%")
        self.log(f"   - ✅ 传统修复率: {trad_rate:.2f}%")
        self.log(f"   - 🧠 动态修复率: {dyn_rate:.2f}%")
        self.log(f"   - 🏁 综合修复率: {total_rate:.2f}%")

        return all_results
