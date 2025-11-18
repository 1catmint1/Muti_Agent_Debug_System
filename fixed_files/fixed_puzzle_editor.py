"""
拼图编辑器 - 核心功能模块
负责业务逻辑，驱动 UI 模块。
"""

import json
import os
import uuid
from PIL import Image
import sys

# --- 核心逻辑类 ---
class PuzzleEditor:
    """拼图编辑器核心逻辑"""
    def __init__(self, main_screen, audio_manager=None):
        """
        初始化编辑器核心
        :param main_screen: 主程序的 Pygame screen 对象
        """
        self.image = None
        self.puzzle_id = None
        self.puzzle_shape = "方形"  # 默认形状
        self.order = 3
        self.main_screen = main_screen # 保存主屏幕引用
        self.ui = None # UI 实例将在 run_editor 中创建
        self.running = True # 控制 UI 循环是否继续
        # 预览区尺寸 (与 puzzle_editor_ui.py 中保持一致)
        self.preview_size = min(400, 700 - 80) # SCREEN_HEIGHT=700, 80是上下边距

        # --- 新增/修改的属性 ---
        # 预览区的最大尺寸限制 (宽, 高)
        self.max_preview_size = (600, 600)
        # 预览区的实际尺寸 (初始为最大尺寸，后续会根据图片调整)
        self.preview_size = self.max_preview_size

        self.audio_manager = audio_manager

    def run_editor(self):
        """启动编辑器 UI"""
        # 导入 UI 模块 (避免循环导入)
        try:
            from ui.puzzle_editor_ui import PuzzleEditorUI
        except ImportError:
             # 如果直接运行此文件，尝试添加父目录到路径
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from ui.puzzle_editor_ui import PuzzleEditorUI

        print("【信息】启动拼图编辑器...")
        self.ui = PuzzleEditorUI(self.main_screen, self) # 创建 UI 实例并传入 self
        self.ui.run() # 启动 UI 循环
        print("【信息】拼图编辑器已关闭。")

    def return_to_menu(self):
        """
        UI 回调：返回主菜单
        退出当前编辑器 UI，控制权交还给主程序。
        """
        print("【UI 回调】返回主菜单...")
        self.running = False  # ✅ 关键：停止 UI 循环
    # 注意：self.ui.run() 循环结束后，会自动返回到 run_editor() 的下一行

    # --- UI 回调方法 (供 UI 模块调用) ---
    def on_ui_quit(self):
        """当 UI 触发退出时调用"""
        self.running = False
        print("【信息】UI 请求退出。")

    def load_image_ui(self):
        """UI 触发的加载图片操作"""
        print("【UI 回调】加载图片...")
        # 使用 Tkinter 打开文件对话框
        # 注意：这会阻塞 Pygame 事件循环，但这是 Tkinter 的常见用法
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw() # 隐藏主窗口
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        root.destroy()
        if file_path:
            success = self._load_image_internal(file_path)
            if success:
                self._clear_state_after_image_load()
                print(f"【信息】图片加载成功: {file_path}")
                # 通知 UI 更新预览区尺寸
                if self.ui:
                     self.ui.on_image_loaded()
            else:
                print("【错误】图片加载失败")

    # --- 修改后的UI回调方法 ---
    def setup_puzzle_ui(self):
        """UI 触发的设置拼图操作（合并后的新按钮）"""
        print("【UI 回调】设置拼图形状和数量...")
        status = self.get_status()
        if not status["has_image"]:
            print("【警告】请先导入图片")
            return

        from tkinter import simpledialog, Tk, Toplevel, StringVar, Button, Label, OptionMenu
        root = Tk()
        root.withdraw()

        # 步骤1: 选择形状
        shape_window = Toplevel(root)
        shape_window.title("选择拼图形状")
        shape_window.geometry("300x150")
        shape_window.resizable(False, False)

        shape_var = StringVar(shape_window)
        shape_var.set("方形")  # 默认值

        Label(shape_window, text="请选择拼图形状:").pack(pady=10)
        shape_menu = OptionMenu(shape_window, shape_var, "方形", "三角形", "不规则")
        shape_menu.pack(pady=5)

        def on_shape_selected():
            selected_shape = shape_var.get()
            shape_window.destroy()

            # 步骤2: 输入阶数/数量
            count_window = Toplevel(root)
            count_window.title("输入拼图阶数")
            count_window.geometry("300x150")
            count_window.resizable(False, False)

            count_var = StringVar(count_window)

            label_text = f"请输入{selected_shape}拼图阶数（3-5）："
            min_val, max_val = 3, 5

            Label(count_window, text=label_text).pack(pady=10)
            entry = simpledialog.Entry(count_window, textvariable=count_var)
            entry.pack(pady=5)
            entry.focus()

            def on_count_enter(event=None): # 支持回车确认
                try:
                    count = int(count_var.get())
                    if min_val <= count <= max_val:
                        count_window.destroy()
                        root.destroy()
                        self.puzzle_shape = selected_shape
                        self.order = count
                        print(f"【信息】已创建 {selected_shape} 拼图, 参数: {count}")
                    else:
                         print(f"【警告】输入值超出范围 ({min_val}-{max_val})")
                         count_window.destroy()
                         root.destroy()
                except ValueError:
                    print("【警告】请输入有效的数字")
                    count_window.destroy()
                    root.destroy()

            entry.bind('<Return>', on_count_enter)
            Button(count_window, text="确定", command=on_count_enter).pack(pady=5)

            count_window.grab_set() # 模态窗口
            count_window.wait_window() # 等待窗口关闭

        Button(shape_window, text="下一步", command=on_shape_selected).pack(pady=10)

        shape_window.grab_set() # 模态窗口
        shape_window.wait_window() # 等待窗口关闭

    def save_settings_ui(self):
        """UI 触发的保存设置操作"""
        print("【UI 回调】保存设置...")
        status = self.get_status()
        if not status["has_image"]:
            print("【警告】请先设置拼图")
            return

        result = self._save_settings_internal()
        if result:
            puzzle_id = result[0]
            print(f"【信息】拼图设置已保存，ID: {puzzle_id}")
            # 可以在这里添加 UI 反馈，例如弹出消息框
            # 但通常由 UI 模块处理，这里只是打印日志
        else:
            print("【错误】拼图设置保存失败")

    # --- 内部核心逻辑方法 ---
    def _load_image_internal(self, image_path):
        """内部加载图片逻辑，并自适应预览区尺寸和比例"""
        try:
            original_image = Image.open(image_path)

            # 1. 先将图片缩放到最大尺寸限制内，保持宽高比
            original_image.thumbnail(self.max_preview_size, Image.Resampling.LANCZOS)

            # 2. 根据缩放后的图片尺寸，计算预览区的实际尺寸 (保持图片宽高比)
            img_width, img_height = original_image.size
            max_width, max_height = self.max_preview_size

            # 计算宽高比
            img_ratio = img_width / img_height
            max_ratio = max_width / max_height

            # 根据图片宽高比和最大区域宽高比，确定最终预览区尺寸
            if img_ratio > max_ratio:
                # 图片更宽，以宽度为准
                final_width = max_width
                final_height = int(max_width / img_ratio)
            else:
                # 图片更高或相等，以高度为准
                final_height = max_height
                final_width = int(max_height * img_ratio)

            # 更新预览区尺寸
            self.preview_size = (final_width, final_height)

            # 3. 将图片调整到最终的预览区尺寸 (可能需要轻微拉伸以精确匹配)
            #    如果希望严格保持比例，可以使用 fit 并添加背景色
            #    这里我们选择 resize 以完全填充预览区
            self.image = original_image.resize(self.preview_size, Image.Resampling.LANCZOS)
            # 或者使用 fit 来保持比例并填充 (需要指定填充颜色)
            # self.image = ImageOps.fit(original_image, self.preview_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            # ImageOps.fit 会裁剪图片，可能不是用户想要的。resize 会轻微拉伸但保证完全填充。
            # 这里我们选择 resize。

            return True
        except Exception as e:
            print(f"【错误】无法加载或调整图片: {e}")
            return False

    def _clear_state_after_image_load(self):
        """加载图片后重置状态"""
        # 注意：不要重置 self.preview_size，因为它现在由图片决定
        self.puzzle_id = None
        self.puzzle_shape = "方形"

    def get_preview_image(self):
        """获取整体预览图 (供 UI 调用)"""
        if self.image:
             return self.image.copy() # UI 会根据 self.image.size 来调整显示
        return None

    def _save_settings_internal(self, base_dir="assets/custom"):
        """内部保存拼图设置逻辑"""
        if not self.image:
            print("【警告】没有拼图设置可保存")
            return None

        # 生成唯一ID
        self.puzzle_id = str(uuid.uuid4())[:8]

        # 创建保存目录
        save_dir = os.path.join(base_dir, self.puzzle_id)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 保存设置信息
        settings = {
            "id": self.puzzle_id,
            "shape": self.puzzle_shape,
            "order": self.order
        }

        # 保存经过调整后的图片 (适应预览区尺寸和比例)
        adjusted_image_path = os.path.join(save_dir, "original.png")
        # self.image 是经过 resize 处理后的图像
        self.image.save(adjusted_image_path, "PNG")
        settings["image_path"] = adjusted_image_path # 保存调整后的图片路径

        # 保存设置文件
        settings_path = os.path.join(save_dir, "settings.json")
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)

        print(f"【信息】拼图设置已保存至: {save_dir}")
        return self.puzzle_id, save_dir

    def get_status(self):
        """获取编辑器状态 (供 UI 调用)"""
        return {
            "has_image": self.image is not None,
            "image": self.image,
            "puzzle_id": self.puzzle_id,
            "puzzle_shape": self.puzzle_shape,
            "order": self.order,
            "preview_size": self.preview_size # 新增：向UI提供预览区尺寸
        }