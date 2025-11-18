import os
import re
import json
import sys
from datetime import datetime
from tkinter import Tk, filedialog

# ---------------------------------------------------------------
# 规则解释（自动生成“为什么错了 / 如何修复”）
# ---------------------------------------------------------------
RULE_EXPLANATION = {
    "PY100": ("未定义名称", "可能使用了未导入的类/函数，或错误拼写，应检查是否需要 import 或修正变量名。"),
    "AST002": ("使用 is 比较", "is 只用于身份比较（None、True、False），值比较应该用 ==。"),
    "AST001": ("可变默认参数", "函数默认值不应使用 list/dict，应替换为 None 并在内部初始化。"),
    "PY010": ("裸 except", "不建议使用 except:，应捕获 Exception 或更精确的异常类型。"),
    "PY011": ("宽泛异常捕获", "捕获 Exception 太宽泛，应替换为具体异常类型。"),
    "PY003": ("shell=True 安全风险", "subprocess 使用 shell=True 会有命令注入风险，应避免。"),
    "PY001": ("eval 风险", "eval 能执行任意代码，应改为 safer 的 ast.literal_eval。"),
}

def explain_rule(rule_id):
    if rule_id in RULE_EXPLANATION:
        title, detail = RULE_EXPLANATION[rule_id]
        return f"**{title}**：{detail}"
    return "（暂无更具体的错误解释）"

# ---------------------------------------------------------------
# 提取 md 中的 JSON
# ---------------------------------------------------------------
def extract_json_from_md(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"```json(.*?)```", content, re.S)
    if not match:
        raise ValueError("在 markdown 中未找到 ```json ... ``` 结构")

    json_str = match.group(1).strip()
    return json.loads(json_str)

# ---------------------------------------------------------------
# 输出人类可读的 Markdown (已移除错误解释和修复建议)
# ---------------------------------------------------------------
def build_human_readable_report(data, output_path):
    lang = list(data["by_language"].keys())[0]
    issues_by_file = data["by_language"][lang]["issues_by_file"]

    lines = []
    lines.append("# 🧾 人类可读版代码问题报告\n")
    lines.append(f"**生成时间**：{datetime.now()}\n")
    lines.append("---\n")

    # 汇总信息
    summary = data["summary"]
    lines.append("## 📊 问题统计\n")
    lines.append(f"- 总问题数：{summary['total_issues']}")
    lines.append(f"- 高危：{summary['high_priority']}")
    lines.append(f"- 中危：{summary['medium_priority']}")
    lines.append(f"- 低危：{summary['low_priority']}\n")

    # 每文件展开
    for filename, issues in issues_by_file.items():
        lines.append(f"\n# 📄 文件：{filename} （共 {len(issues)} 个问题）\n")

        for idx, issue in enumerate(issues, 1):
            file = issue.get("file", filename)
            line_no = issue.get("line")
            snippet = issue.get("snippet")
            rule = issue.get("rule_id") or issue.get("code")
            message = issue.get("message")

            lines.append(f"## 🔹 问题 {idx}\n")
            lines.append(f"- **规则**：`{rule}`")
            lines.append(f"- **位置**：{file}:{line_no}")
            lines.append(f"- **描述**：{message}\n")

            # 原始代码
            if snippet:
                lines.append("### 🔍 原始代码\n")
                lines.append("```python")
                lines.append(snippet)
                lines.append("```")

            lines.append("\n---\n")

    # 保存文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


# ---------------------------------------------------------------
# 主入口：支持文件选择窗口
# ---------------------------------------------------------------
def main():
    # 如果命令行传了参数，优先使用
    if len(sys.argv) > 1:
        md_path = sys.argv[1]
    else:
        # 弹出选择文件窗口
        Tk().withdraw()
        md_path = filedialog.askopenfilename(
            title="请选择包含 JSON 的 Markdown 报告文件",
            filetypes=[("Markdown 文件", "*.md"), ("所有文件", "*.*")]
        )

        if not md_path:
            print("未选择文件，已退出。")
            return

    if not os.path.exists(md_path):
        print("文件不存在：", md_path)
        return

    print(f"[INFO] 正在解析：{md_path}")

    # 创建输出目录
    out_dir = os.path.join(os.getcwd(), "reports_parsed")
    os.makedirs(out_dir, exist_ok=True)

    try:
        data = extract_json_from_md(md_path)
    except Exception as e:
        print("无法解析 JSON：", e)
        return

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = os.path.join(out_dir, f"readable_report_{ts}.md")

    final = build_human_readable_report(data, out_path)

    print("\n[OK] 已生成可读版报告：")
    print(final)


if __name__ == "__main__":
    main()