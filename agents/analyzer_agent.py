# agents/analyzer_agent.py
"""
AnalyzerAgent - 多语言代码分析Agent
"""
import sys
import os
from typing import Dict, Any, List
DEBUG_ANALYZER = os.environ.get("ANALYZER_DEBUG", "0") == "1"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent
from utils.language_detector import Language, LanguageDetector


class AnalyzerAgent(BaseAgent):
    """多语言代码分析Agent"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("AnalyzerAgent", config or {})
        self.analysis_results = {}

    def perceive(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """感知阶段：接收扫描结果"""
        scan_results = input_data.get("scan_results", {})
        files = input_data.get("files", [])

        # 统计信息
        summary = scan_results.get("summary", {})
        total_defects = summary.get("total_defects", 0)
        by_language = summary.get("by_language", {})

        self.log(f"📊 收到扫描结果：总计 {total_defects} 个问题")

        if by_language:
            self.log(f"   按语言分布：")
            # ✅ 处理两种可能的数据格式
            for lang, stats in by_language.items():
                if isinstance(stats, dict):
                    # 字典格式：{"total": 100, ...}
                    count = stats.get('total', 0)
                elif isinstance(stats, int):
                    # 整数格式：100
                    count = stats
                else:
                    count = 0

                self.log(f"      • {lang.upper()}: {count} 个")

        return {
            "scan_results": scan_results,
            "files": files,
            "total_defects": total_defects,
            "by_language": scan_results.get("by_language", {})  # ✅ 使用完整数据
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """决策阶段：分析问题优先级和修复策略"""
        by_language = perception.get("by_language", {})

        # 如果没有问题，直接返回
        if not by_language or perception.get("total_defects", 0) == 0:
            self.log("\n✅ 未发现问题，无需分析")
            return {
                "fix_plans": [],
                "priority_order": [],
                "recommendations": []
            }

        strategy = {
            "fix_plans": [],
            "priority_order": [],
            "recommendations": []
        }

        # 为每种语言制定修复计划
        for lang_name, lang_results in by_language.items():
            # ✅ 处理可能的错误情况
            if "error" in lang_results:
                self.log(f"⚠️ {lang_name.upper()} 扫描失败，跳过分析")
                continue

            summary = lang_results.get("summary", {})

            if summary.get("total", 0) == 0:
                continue

            # 获取严重程度统计
            builtin = lang_results.get("builtin", [])
            external = lang_results.get("external", [])

            # ✅ 统计严重程度（处理字符串和字典）
            high_count = 0
            medium_count = 0
            low_count = 0

            for issue in builtin + external:
                if isinstance(issue, dict):
                    severity = issue.get("severity", "LOW")
                elif isinstance(issue, str):
                    # 从字符串判断严重程度
                    severity = "MEDIUM"
                    if any(kw in issue.lower() for kw in ["error", "critical", "fatal"]):
                        severity = "HIGH"
                    elif any(kw in issue.lower() for kw in ["warning", "info"]):
                        severity = "LOW"
                else:
                    severity = "LOW"

                if severity == "HIGH":
                    high_count += 1
                elif severity == "MEDIUM":
                    medium_count += 1
                else:
                    low_count += 1

            # 计算优先级得分
            priority_score = high_count * 10 + medium_count * 5 + low_count * 1

            fix_plan = {
                "language": lang_name,
                "total_issues": summary.get("total", 0),
                "high": high_count,
                "medium": medium_count,
                "low": low_count,
                "priority_score": priority_score,
                "builtin_issues": builtin,
                "external_issues": external,
                "dynamic_results": lang_results.get("dynamic", {}),
            }

            strategy["fix_plans"].append(fix_plan)

        # 按优先级排序
        strategy["fix_plans"].sort(key=lambda x: x["priority_score"], reverse=True)
        strategy["priority_order"] = [plan["language"] for plan in strategy["fix_plans"]]

        # 生成建议
        for plan in strategy["fix_plans"]:
            lang = plan["language"]

            if plan["high"] > 0:
                strategy["recommendations"].append(
                    f"⚠️ {lang.upper()}: 发现 {plan['high']} 个高危问题，建议优先修复"
                )

            dynamic_results = plan["dynamic_results"]
            if isinstance(dynamic_results, dict) and not dynamic_results.get("compile_success", True):
                strategy["recommendations"].append(
                    f"❌ {lang.upper()}: 代码存在编译错误，需要先修复语法问题"
                )

        self.log(f"\n决策：制定了 {len(strategy['fix_plans'])} 个修复计划")
        if strategy['priority_order']:
            self.log(f"优先级顺序：")
            for i, lang in enumerate(strategy['priority_order'], 1):
                plan = next(p for p in strategy['fix_plans'] if p['language'] == lang)
                self.log(f"   {i}. {lang.upper()}: {plan['total_issues']} 个问题 "
                         f"(HIGH={plan['high']}, MEDIUM={plan['medium']}, LOW={plan['low']})")

        # ==========================================================
        # 🔧 自动构建 issues_by_file，确保 FixerAgent 可读取
        # ==========================================================
        by_language_with_files = {}
        for plan in strategy["fix_plans"]:
            lang = plan["language"]
            builtin = plan.get("builtin_issues", [])
            external = plan.get("external_issues", [])
            all_issues = builtin + external

            issues_by_file = {}
            for issue in all_issues:
                file = "unknown"

                # ✅ 情况1：字典
                if isinstance(issue, dict):
                    raw_file = issue.get("file") or issue.get("filename") or issue.get("path")
                    if raw_file:
                        file = os.path.basename(str(raw_file))
                    elif "Finding" in str(type(issue)):
                        # 针对 dataclass/Finding 对象转 dict
                        file = getattr(issue, "file", getattr(issue, "filename", "unknown")) or "unknown"

                # ✅ 情况2：自定义对象（如 PMD Finding）
                elif hasattr(issue, "__dict__"):
                    # 通常 PMD 的 Finding 对象有 file、filename、message 等属性
                    file = getattr(issue, "file", getattr(issue, "filename", "unknown"))
                    if not file:
                        file = "unknown"

                # ✅ 情况3：字符串
                elif isinstance(issue, str):
                    parts = issue.split(":") if ":" in issue else []
                    file = os.path.basename(parts[0].strip()) if parts else "unknown"

                issues_by_file.setdefault(file, []).append(issue)

            by_language_with_files[lang] = {
                "total": plan["total_issues"],
                "issues_by_file": issues_by_file,
                "summary": {
                    "high": plan["high"],
                    "medium": plan["medium"],
                    "low": plan["low"]
                }
            }

        # 将该结构写入 self.analysis_results，供后续阶段调用
        self.analysis_results = {"by_language": by_language_with_files}
        # ==========================================================


        return strategy

    # agents/analyzer_agent.py

    def execute(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """执行阶段：生成详细的分析报告（兼容 Finding、dict、str 三种格式）"""
        fix_plans = decision.get("fix_plans", [])
        recommendations = decision.get("recommendations", [])

        analysis_report = {
            "summary": {
                "total_languages": len(fix_plans),
                "total_issues": sum(plan.get("total_issues", 0) for plan in fix_plans),
                "high_priority": sum(plan.get("high", 0) for plan in fix_plans),
                "medium_priority": sum(plan.get("medium", 0) for plan in fix_plans),
                "low_priority": sum(plan.get("low", 0) for plan in fix_plans),
            },
            "by_language": {},
            "recommendations": recommendations,
            "fix_plans": fix_plans
        }

        # =============================
        # 🔍 按语言分组问题
        # =============================
        for plan in fix_plans:
            lang = plan["language"]
            builtin_issues = plan.get("builtin_issues", [])
            external_issues = plan.get("external_issues", [])
            all_issues = builtin_issues + external_issues

            issues_by_file = {}

            for issue in all_issues:
                file = "unknown"

                # ✅ 1. 字典类型
                if isinstance(issue, dict):
                    raw_file = issue.get("file") or issue.get("filename") or issue.get("path")
                    if raw_file:
                        file = os.path.basename(str(raw_file))

                # ✅ 2. PMD/Finding 对象（dataclass 或 namedtuple）
                elif hasattr(issue, "__dict__") or "Finding" in str(type(issue)):
                    # 安全获取属性
                    file = getattr(issue, "file", None) or getattr(issue, "filename", None) or "unknown"
                    file = os.path.basename(str(file)) if file else "unknown"

                # ✅ 3. 字符串类型
                elif isinstance(issue, str):
                    parts = issue.split(":") if ":" in issue else []
                    file = os.path.basename(parts[0].strip()) if parts else "unknown"

                issues_by_file.setdefault(file, []).append(issue)

            # =============================
            # 🔍 调试输出：文件分布
            # =============================
            if DEBUG_ANALYZER:
                print(f"\n[AnalyzerAgent] {lang.upper()} 问题分组结果：")
                for fname, issue_list in sorted(issues_by_file.items()):
                    print(f"  - {fname}: {len(issue_list)} 个问题")
                    # 打印前三条
                    for ex in issue_list[:3]:
                        msg = ""
                        if isinstance(ex, dict):
                            msg = ex.get("message", "")
                        elif hasattr(ex, "message"):
                            msg = getattr(ex, "message", "")
                        else:
                            msg = str(ex)
                        print(f"      → {msg[:120]}")

            # =============================
            # ⚙️ 按严重程度分组
            # =============================
            issues_by_severity = {"HIGH": [], "MEDIUM": [], "LOW": []}

            for issue in all_issues:
                if isinstance(issue, dict):
                    severity = issue.get("severity", "LOW")
                elif hasattr(issue, "severity"):
                    severity = getattr(issue, "severity", "LOW")
                else:
                    s = str(issue).lower()
                    if any(k in s for k in ["error", "critical", "fatal"]):
                        severity = "HIGH"
                    elif any(k in s for k in ["warning", "info"]):
                        severity = "LOW"
                    else:
                        severity = "MEDIUM"

                issues_by_severity.setdefault(severity, []).append(issue)

            analysis_report["by_language"][lang] = {
                "total": plan.get("total_issues", len(all_issues)),
                "issues_by_file": issues_by_file,
                "issues_by_severity": issues_by_severity,
                "dynamic_check": plan.get("dynamic_results", {})
            }

        # =============================
        # ✅ 汇总日志
        # =============================
        self.log("\n✅ 分析完成！")
        self.log(f"   - 涉及语言: {analysis_report['summary']['total_languages']} 种")
        self.log(f"   - 总问题数: {analysis_report['summary']['total_issues']} 个")
        self.log(f"   - 优先级分布: HIGH={analysis_report['summary']['high_priority']}, "
                 f"MEDIUM={analysis_report['summary']['medium_priority']}, "
                 f"LOW={analysis_report['summary']['low_priority']}")

        if recommendations:
            self.log("\n📌 建议：")
            for rec in recommendations:
                self.log(f"   {rec}")

        return analysis_report




# 兼容旧版本的analyze方法
def analyze_defects(defects: List[Dict], files: List[Dict]) -> Dict[str, Any]:
    """旧版本兼容接口"""
    agent = AnalyzerAgent()

    # 构造输入
    input_data = {
        "scan_results": {
            "defects": defects,
            "summary": {
                "total_defects": len(defects),
                "by_language": {}
            }
        },
        "files": files
    }

    perception = agent.perceive(input_data)
    decision = agent.decide(perception)
    result = agent.execute(decision)

    return result