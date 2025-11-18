# -- coding:UTF-8 --
# Author: lintx
# Date: 2025/02/10

import sys
import os
import json
import glob
from datetime import datetime
import contextlib

# PyQt5 GUI 相关导入
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


def ask(prompt: str) -> bool:
    """终端 yes/no 提示"""
    ans = input("是否运行 DebugBench 多Agent 评测？ [y/n]: ").strip().lower()

    import builtins
    if ans == "y":
        print("⚠️ 已启用debugbench测试")
        builtins.DEBUGBENCH_SKIP_COMPILE = True
        builtins.DEBUGBENCH_USE_LLM_VERIFY = True
        return True
    else:
        print("✔ 将使用正常编译与功能测试验证")
        builtins.DEBUGBENCH_SKIP_COMPILE = False
        builtins.DEBUGBENCH_USE_LLM_VERIFY = False
        return False


# 自定义输出流：同时向终端和文件输出
class Tee:
    def __init__(self, file_handle, terminal_handle):
        self.file = file_handle
        self.terminal = terminal_handle

    def write(self, message):
        # 同时写入终端和文件
        self.terminal.write(message)
        self.file.write(message)
        # 确保内容即时刷新
        self.terminal.flush()
        self.file.flush()

    def flush(self):
        self.terminal.flush()
        self.file.flush()


# 自定义上下文管理器：同时输出到终端和文件
@contextlib.contextmanager
def tee_output(file_path):
    """将输出同时发送到终端和文件"""
    # 保存原始输出流
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    # 创建文件句柄
    with open(file_path, 'w', encoding='utf-8') as f:
        # 创建分流输出器
        sys.stdout = Tee(f, original_stdout)
        sys.stderr = Tee(f, original_stderr)
        try:
            yield  # 执行with块中的代码
        finally:
            # 恢复原始输出流
            sys.stdout = original_stdout
            sys.stderr = original_stderr


def detect_lang_from_filename(filename: str) -> str:
    """
    根据 DebugBench 原始 json 文件名判断语言：
    - cpp_xxx.json  -> "cpp"
    - java_xxx.json -> "java"
    - python3_xxx.json -> "python"
    """
    base = os.path.basename(filename).lower()
    if base.startswith("cpp_"):
        return "cpp"
    if base.startswith("java_"):
        return "java"
    if base.startswith("python3_"):
        return "python"
    # 兜底：按 C++ 处理
    return "cpp"


def load_debugbench(debugbench_path):
    """从指定目录加载 DebugBench JSON（每个文件含多条样本），并基于文件名标注语言"""
    if not debugbench_path:
        # 如果没有输入路径，使用默认路径
        debugbench_path = r"C:\Users\lenovo\Desktop\link-tools-main\DebugBench-main\benchmark"
    
    if not os.path.isdir(debugbench_path):
        print(f"❌ 目录不存在: {debugbench_path}")
        return []

    dataset = []

    for file in glob.glob(os.path.join(debugbench_path, "*.json")):
        lang = detect_lang_from_filename(file)
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            # 如果样本本身没有 language 字段，则根据文件名添加
                            item.setdefault("language", lang)
                            dataset.append(item)
                elif isinstance(data, dict):
                    data.setdefault("language", lang)
                    dataset.append(data)
                else:
                    # 非 dict/列表的不管了
                    pass
        except Exception as e:
            print(f"⚠️ 文件解析失败：{file}: {e}")

    print(f"📦 已加载 {len(dataset)} 条 DebugBench 样本（展开后，并已按文件名标记 language）\n")
    return dataset


def run_debugbench_terminal():
    """终端运行 DebugBench 评测"""
    # 动态导入，避免在GUI模式下加载
    from run_debugbench_agent import run_debugbench_with_agents
    
    # 获取用户输入的 DebugBench 路径
    print("\n=== 配置 DebugBench 路径 ===")
    debugbench_path = input(f"请输入 DebugBench 数据集路径 ]: ").strip()
    
    # 获取用户输入的模型名称
    print("\n=== 配置 Ollama 模型 ===")
    default_model = "qwen3-coder:30b"
    model_name = input(f"请输入 Ollama 模型名称 [回车使用默认: {default_model}]: ").strip()
    if not model_name:
        model_name = default_model
    
    # 创建结果文件，使用当前时间作为文件名一部分
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = f"debugbench_terminal_output_{timestamp}.txt"
    
    print(f"\n📄 所有输出将同时显示在终端并保存至: {os.path.abspath(result_file)}\n")
    
    # 使用分流上下文管理器：同时输出到终端和文件
    with tee_output(result_file):
        print("\n================================")
        print("🚀 DebugBench × 多Agent 终端评测启动")
        print("================================\n")
        print(f"📁 DebugBench 路径: {debugbench_path}")
        print(f"🤖 使用模型: {model_name}")
        print("================================\n")

        # 读取 LLM 配置
        model_api = load_model_config(model_name)

        # 加载 DebugBench
        dataset = load_debugbench(debugbench_path)
        if not dataset:
            print("⚠️ 未加载到任何样本，退出。")
            return

        # 运行多Agent评测
        correct_strict, correct_ast, total, stats = run_debugbench_with_agents(
            dataset=dataset,
            samples_per_lang=30,
            model_api=model_api
        )

        print("\n" + "=" * 50)
        print(f"🎉 DebugBench 测试完成")
        if total > 0:
            print(f"✨ 严格修复率: {correct_strict}/{total} = {correct_strict/total:.4f}")
            print(f"✨ AST 修复率: {correct_ast}/{total} = {correct_ast/total:.4f}")
        else:
            print("✨ 修复率: N/A")
        print("=" * 50 + "\n")
    
    # 额外提示文件保存位置（已在分流中输出过，这里可省略）
    print(f"\n✅ 评测完成，输出已保存至: {os.path.abspath(result_file)}")


def load_model_config(model_name):
    """读取 LLM 配置"""
    print("\n=== 配置 LLM 模型 ===")
    # 使用用户输入的模型名称
    api_base = "http://localhost:11434/api/chat"
    api_key = input("API Key（OpenAI 才需要，没有就回车）: ").strip()

    return {
        "api_base": api_base,
        "api_key": api_key,
        "model": model_name
    }


def run_gui_application():
    """运行 GUI 应用程序"""

    # 导入 GUI 相关模块（在需要时才导入）
    from tabs.ui_main import Ui_Form

    # 只加载 TabAI
    try:
        from tabs.tab_ai import EnhancedTabAI
    except ImportError:
        from tabs.tab_ai import tab_ai as EnhancedTabAI

    class MyMainForm(QMainWindow, Ui_Form):
        def __init__(self, parent=None):
            super(MyMainForm, self).__init__(parent)
            self.setupUi(self)

            # -------------------------------------------
            # 删除 UI 中不需要的 tab（保持 UI 文件不变）
            # -------------------------------------------
            self.tabWidget.removeTab(0)
            self.tabWidget.removeTab(0)

            # AI 功能加载
            self.tab_ai = EnhancedTabAI(self)

            # combobox 只需要一个名字
            self.tabs_combox.clear()
            self.tabs_combox.addItem("AI")
            self.tabs_combox.setCurrentText("AI")

            # 保存按钮
            self.tabs_button.clicked.connect(self.tabs_save)

            tabs_settings = QSettings("link_tools", "AI")
            tabs_cname = tabs_settings.value("tabs_cname", "AI")
            self.tabs_combox.setCurrentText(tabs_cname)
            self.tabWidget.setCurrentIndex(0)

            try:
                self.tabread()
                self.tabWidget.currentChanged.connect(self.tabread)
            except Exception as e:
                QMessageBox.about(self, "错误", f"配置文件缺失，请检查config目录\n{e}")
                exit()

        # -------------------------------------------
        # 只处理 AI tab
        # -------------------------------------------
        def tabread(self):
            os.chdir(pwd)
            if hasattr(self.tab_ai, "on_tab_shown"):
                self.tab_ai.on_tab_shown()

        def tabs_save(self):
            tabs_settings = QSettings("link_tools", "AI")
            tabs_settings.setValue("tabs_cname", "AI")
            QMessageBox.information(self, "提示", "配置保存成功！")

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    pwd = os.getcwd()
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    # 先生成结果文件名（即使不用）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = f"debugbench_terminal_output_{timestamp}.txt"
    
    print(f"======= Link-Tools Terminal Version =======")
    
    # 先询问用户选择
    run_debugbench = ask("是否运行 DebugBench 多Agent 评测？")
    
    if run_debugbench:
        # 运行 DebugBench 模式（使用输出重定向）
        with tee_output(result_file):
            run_debugbench_terminal()
        print(f"\n✅ 程序结束，输出已保存至: {os.path.abspath(result_file)}")
    else:
        # 运行 GUI 模式（不使用输出重定向）
        print("启动 GUI 界面...")
        run_gui_application()