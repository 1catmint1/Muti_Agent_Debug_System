"""
OrchestratorAgent - 多语言Bug修复系统的总协调器
"""
import sys
import os
import re
from typing import Dict, Any, List
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent
from .scanner_agent import ScannerAgent
from .analyzer_agent import AnalyzerAgent
from .fixer_agent import FixerAgent
from .verifier_agent import VerifierAgent


class OrchestratorAgent(BaseAgent):
    """总协调器Agent - 协调多语言Bug修复流程"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("OrchestratorAgent", config or {})

        # 初始化子Agent
        self.scanner = ScannerAgent(config.get("scanner", {}) if config else {})
        self.analyzer = AnalyzerAgent(config.get("analyzer", {}) if config else {})
        self.fixer = FixerAgent(config.get("fixer", {}) if config else {})
        self.verifier = VerifierAgent(config.get("verifier", {}) if config else {})

        self.workflow_state = {}

    def perceive(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """感知阶段：接收用户输入"""
        files = input_data.get("files", [])
        user_request = input_data.get("user_request", "")
        test_cases = input_data.get("test_cases", [])

        self.log("=" * 80)
        self.log("🚀 多语言Bug检测与修复系统启动")
        self.log("=" * 80)
        self.log(f"\n📂 收到文件: {len(files)} 个")
        for f in files[:20]:  # 只显示前20个
            self.log(f"   - {f.get('file', 'unknown')}")
        if len(files) > 20:
            self.log(f"   ... 还有 {len(files) - 20} 个文件")

        if user_request:
            if user_request:
                cleaned_request = user_request
                cleaned_request = re.sub(
                    r"【重要提示】.*?【提示结束】",
                    "",
                    cleaned_request,
                    flags=re.S
                )
                cleaned_request = re.sub(
                    r"【任务/问题提示】.*?【任务提示结束】",
                    "",
                    cleaned_request,
                    flags=re.S
                )

                self.log(f"\n📝 用户需求: {cleaned_request}")

        if test_cases:
            self.log(f"\n🧪 测试用例: {len(test_cases)} 个")

        return {
            "files": files,
            "user_request": user_request,
            "test_cases": test_cases,
            "enable_scanner": self.config.get("enable_scanner", True),
            "enable_analyzer": self.config.get("enable_analyzer", True),
            "enable_fixer": self.config.get("enable_fixer", True),
            "enable_verifier": self.config.get("enable_verifier", True),
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """决策阶段：制定执行计划"""
        strategy = {
            "workflow": [],
            "enable_agents": {}
        }

        # 构建工作流
        if perception.get("enable_scanner", True):
            strategy["workflow"].append("scan")
            strategy["enable_agents"]["scanner"] = True

        if perception.get("enable_analyzer", True):
            strategy["workflow"].append("analyze")
            strategy["enable_agents"]["analyzer"] = True

        if perception.get("enable_fixer", True):
            strategy["workflow"].append("fix")
            strategy["enable_agents"]["fixer"] = True

        if perception.get("enable_verifier", True):
            strategy["workflow"].append("verify")
            strategy["enable_agents"]["verifier"] = True

        self.log(f"\n📋 执行计划：{' -> '.join(strategy['workflow'])}")

        return strategy

        # agents/orchestrator_agent.py

    def execute(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """执行阶段：协调各Agent执行 (带自愈循环 & 结果累积)"""
        workflow = decision.get("workflow", [])
        enable_agents = decision.get("enable_agents", {})

        # 🔥🔥🔥 1. 初始化累积字典：用于跨轮次保存所有文件的最新修复状态
        # Key: filename, Value: file_result_dict
        accumulated_fixed_files = {}

        # 配置最大重试次数
        MAX_RETRIES = 2

        files = decision.get("files", [])
        # 使用 current_files 追踪代码的最新状态
        current_files = files

        # 结果容器
        final_pipeline_results = {
            "success": False,
            "history": []  # 记录每一轮的结果
        }

        current_analysis = None
        current_dynamic_feedback = None  # 用于传递给 Fixer

        for attempt in range(MAX_RETRIES + 1):  # +1 是因为第0次是正常流程
            self.log(f"\n{'#' * 80}")
            if attempt == 0:
                self.log(f"🔄 执行工作流 (初始轮次)")
            else:
                self.log(f"🔄 执行工作流 (重试轮次 {attempt}/{MAX_RETRIES}) - 尝试修复运行时问题")
            self.log(f"{'#' * 80}")

            # 本轮的结果容器
            round_results = {
                "round": attempt,
                "scan_results": None,
                "fix_results": None,
                "verification": None
            }

            try:
                # 1. 扫描 (仅在第一轮)
                if "scan" in workflow and enable_agents.get("scanner") and attempt == 0:
                    self.log(f"\n🔍 阶段 1/4：代码扫描")
                    # 调用 Scanner
                    scan_input = {"files": current_files}
                    self.scanner.perceive(scan_input)
                    # 执行扫描
                    scan_results = self.scanner.execute(scan_input)
                    round_results["scan_results"] = scan_results

                # 2. 分析 (仅在第一轮)
                if "analyze" in workflow and enable_agents.get("analyzer") and attempt == 0:
                    self.log(f"\n📊 阶段 2/4：缺陷分析")
                    scan_res = round_results.get("scan_results", {})

                    # 调用 Analyzer
                    analyze_input = {
                        "scan_results": scan_res,
                        "files": current_files
                    }
                    analyze_perception = self.analyzer.perceive(analyze_input)
                    analyze_decision = self.analyzer.decide(analyze_perception)
                    # 执行分析
                    current_analysis = self.analyzer.execute(analyze_decision)

                # 3. 修复 (Fixer)
                if "fix" in workflow and enable_agents.get("fixer"):
                    self.log(f"\n🔧 阶段 3/4：代码修复 (Round {attempt})")

                    fix_input = {
                        "analysis": current_analysis,  # 第一轮用的静态分析
                        "files": current_files,  # 最新的文件内容
                        "user_request": decision.get("user_request", ""),
                        # 传入动态反馈 (如果是重试轮次)
                        "dynamic_feedback": current_dynamic_feedback
                    }

                    # Fixer 执行逻辑
                    fix_perception = self.fixer.perceive(fix_input)
                    fix_decision = self.fixer.decide(fix_perception)
                    # 确保传入 files
                    fix_decision.update({"files": current_files})

                    fix_results = self.fixer.execute(fix_decision)
                    round_results["fix_results"] = fix_results

                    # 🔥🔥🔥 2. 更新累积结果 🔥🔥🔥
                    # 无论成功失败，只要 Fixer 返回了该文件的结果，就更新到累积字典中
                    # 这样保证了最后输出的是所有涉及文件的最新状态
                    current_round_fixed = fix_results.get("fixed_files", [])
                    for f in current_round_fixed:
                        filename = f.get("file")
                        if filename:
                            accumulated_fixed_files[filename] = f

                    # 更新 current_files 为修复后的文件 (用于下一轮或验证)
                    current_files = self._update_files_content(current_files, current_round_fixed)

                # 4. 验证 (Verifier) - 包含动态检测
                if "verify" in workflow and enable_agents.get("verifier"):
                    self.log(f"\n✅ 阶段 4/4：验证与动态检测 (Round {attempt})")

                    verify_input = {
                        "fix_results": round_results.get("fix_results", {}),
                        # 注意：Verifier 需要的是 fixed_files (list of dict)
                        "fixed_files": round_results.get("fix_results", {}).get("fixed_files", []),
                        "original_files": files,  # 最原始的文件
                        "test_cases": decision.get("test_cases", []),
                        "attempt": attempt  # 传递轮次
                    }

                    # Verifier 执行逻辑
                    verify_perception = self.verifier.perceive(verify_input)
                    verify_decision = self.verifier.decide(verify_perception)
                    verification_results = self.verifier.execute(verify_decision)

                    round_results["verification"] = verification_results

                    # 检查是否需要重试
                    has_dynamic_issues = verification_results.get("has_dynamic_issues", False)
                    dynamic_report = verification_results.get("dynamic_report", {})

                    # 记录本轮结果到历史
                    final_pipeline_results["history"].append(round_results)

                    if has_dynamic_issues:
                        if attempt < MAX_RETRIES:
                            self.log(f"⚠️ 检测到动态运行时错误，准备进入下一轮修复...")
                            current_dynamic_feedback = dynamic_report
                            continue  # 进入下一次循环
                        else:
                            self.log(f" 达到最大重修次数，动态修复未完全成功。")
                    else:
                        self.log(f"🎉 验证通过！没有发现动态运行时错误。")
                        final_pipeline_results["success"] = True
                        break  # 成功，退出循环

            except Exception as e:
                self.log(f"❌ Round {attempt} 发生错误: {e}")
                import traceback
                traceback.print_exc()
                # 即使出错，也要记录已有的结果
                final_pipeline_results["history"].append(round_results)
                final_pipeline_results["error"] = str(e)
                break

        # --- 循环结束后的结果汇总 ---

        # 🔥🔥🔥 3. 构造最终的 fix_results (从累积字典中) 🔥🔥🔥
        if accumulated_fixed_files:
            final_fixed_files_list = list(accumulated_fixed_files.values())

            if "fix_results" not in final_pipeline_results:
                final_pipeline_results["fix_results"] = {}

            # 强制覆盖为全量累积列表
            final_pipeline_results["fix_results"]["fixed_files"] = final_fixed_files_list

            # 重新计算统计信息
            success_count = sum(1 for f in final_fixed_files_list if f.get("success"))
            failed_count = len(final_fixed_files_list) - success_count

            final_pipeline_results["fix_results"]["summary"] = {
                "total_files": len(final_fixed_files_list),
                "successfully_fixed": success_count,
                "failed": failed_count,
                "total_fixes": sum(f.get("fixed_count", 0) for f in final_fixed_files_list)
            }

        # 🔥🔥🔥 4. 确保 scan_results 存在 (防止 UI 报错) 🔥🔥🔥
        # 如果当前结果中没有 scan_results，尝试从历史记录（通常是第一轮）中找回
        if not final_pipeline_results.get("scan_results") and final_pipeline_results.get("history"):
            for history_round in final_pipeline_results["history"]:
                if history_round.get("scan_results"):
                    final_pipeline_results["scan_results"] = history_round["scan_results"]
                    break

        # 同样确保 verification 也是最新的
        if not final_pipeline_results.get("verification") and final_pipeline_results.get("history"):
            final_pipeline_results["verification"] = final_pipeline_results["history"][-1].get("verification")

        # 生成总结
        self._generate_summary(final_pipeline_results)
        return final_pipeline_results

    def _generate_summary(self, results: Dict[str, Any]):
        """生成执行总结"""
        # 这里的逻辑是为了防止 execution_time 为空导致报错
        exec_time = results.get("execution_time", {})
        # 如果 exec_time 是空的，就设总时间为 0
        total_time = sum(exec_time.values()) if exec_time else 0.0

        self.log("")
        self.log("=" * 80)
        self.log("📊 执行总结")
        self.log("=" * 80)

        self.log("")
        self.log(f"⏱️ 总耗时: {total_time:.2f}秒")

        if total_time > 0:
            for stage, duration in exec_time.items():
                percentage = (duration / total_time * 100)
                self.log(f"   - {stage}: {duration:.2f}秒 ({percentage:.1f}%)")

        # 扫描结果
        #scan_results = results.get("scan_results", {}) or {}
        #scan_summary = scan_results.get("summary", {}) or {}

        #self.log("")
        #self.log("🔍 扫描结果:")
        #self.log(f"   - 发现问题: {scan_summary.get('total_defects', 0)} 个")

        #by_severity = scan_summary.get("by_severity", {}) or {}
        #self.log(f"   - 高危: {by_severity.get('HIGH', 0)} 个")
        #self.log(f"   - 中危: {by_severity.get('MEDIUM', 0)} 个")
        #self.log(f"   - 低危: {by_severity.get('LOW', 0)} 个")

        # 修复结果
        fix_results = results.get("fix_results", {}) or {}
        fix_summary = fix_results.get("summary", {}) or {}

        self.log("")
        self.log("🔧 修复结果:")
        self.log(f"   - 处理文件: {fix_summary.get('total_files', 0)} 个")
        self.log(f"   - 成功修复: {fix_summary.get('successfully_fixed', 0)} 个")
        self.log(f"   - 修复失败: {fix_summary.get('failed', 0)} 个")
        self.log(f"   - 总修复数: {fix_summary.get('total_fixes', 0)} 处")
    def _update_files_content(self, original_files, fixed_files_list):
            """辅助函数：用修复后的内容更新文件列表"""
            # 创建一个 map 方便查找
            fixed_map = {f.get('file'): f.get('content') for f in fixed_files_list if f.get('success')}

            updated = []
            for f in original_files:
                new_f = f.copy()
                fname = f.get('file')
                # 尝试多种匹配策略 (path, basename) 与 FixerAgent 类似
                if fname in fixed_map:
                    new_f['content'] = fixed_map[fname]
                else:
                    # 简单的 fallback，实际情况可能需要更复杂的路径匹配
                    base = os.path.basename(fname)
                    for k, v in fixed_map.items():
                        if os.path.basename(k) == base:
                            new_f['content'] = v
                            break
                updated.append(new_f)
            return updated


def run_multi_language_repair(files: List[Dict],
                              user_request: str = "",
                              test_cases: List[Dict] = None,
                              llm_client=None) -> Dict[str, Any]:
    """
    运行多语言Bug修复流程的便捷函数

    Args:
        files: 文件列表 [{"file": "xxx", "content": "..."}, ...]
        user_request: 用户额外需求
        test_cases: 测试用例
        llm_client: LLM客户端

    Returns:
        完整的执行结果
    """
    config = {
        "fixer": {
            "llm_client": llm_client,
            "use_rules": True,
            "use_llm": llm_client is not None,
            # 🔥 为 Java 启用“无 issue 也尝试 LLM 修复”的兜底策略
            "force_llm_on_empty": {"java": True},
        }
    }

    orchestrator = OrchestratorAgent(config)

    input_data = {
        "files": files,
        "user_request": user_request,
        "test_cases": test_cases or []
    }

    perception = orchestrator.perceive(input_data)
    decision = orchestrator.decide(perception)
    decision.update(perception)
    results = orchestrator.execute(decision)

    return results