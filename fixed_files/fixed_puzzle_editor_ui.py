"""
拼图编辑器 - Pygame UI 模块
负责 UI 渲染和事件处理，由核心逻辑驱动。
"""

import pygame
from tkinter import Tk
from PIL import Image
import os

# --- 导入配置 ---
try:
    import config
    SCREEN_WIDTH = config.SCREEN_WIDTH
    SCREEN_HEIGHT = config.SCREEN_HEIGHT
    PIECE_AREA_HEIGHT = config.PIECE_AREA_HEIGHT
    BACKGROUND_COLOR = config.BACKGROUND_COLOR
    GRID_COLOR = config.GRID_COLOR
    TEXT_COLOR = config.TEXT_COLOR
    HIGHLIGHT_COLOR = config.HIGHLIGHT_COLOR
except ImportError:
    print("【警告】未找到 config.py，使用默认配置。")
    # --- 默认 UI 配置 ---
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 700
    PIECE_AREA_HEIGHT = 200
    BACKGROUND_COLOR = (220, 220, 220)
    GRID_COLOR = (100, 110, 100)  # 修正原代码中颜色值错误
    TEXT_COLOR = (0, 0, 0)
    HIGHLIGHT_COLOR = (255, 255, 0, 150)
    
PIECE_BG_COLOR = (0,0,0,0)

# --- 字体加载 ---
def load_font(font_path, size):
    """加载指定大小的字体"""
    if os.path.exists(font_path):
        return pygame.font.Font(font_path, size)
    else:
        print(f"【警告】未找到字体文件 {font_path}，使用默认字体。")
        return pygame.font.Font(None, size)   

font_size = load_font('zhengwen.ttf', 36)  # 根据需要调整字体大小


class Button:
    """图片按钮类（无文字）"""
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.hovered = False
        self.scale_factor = 1.2  # 悬停时的缩放比例

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        # 根据是否悬停决定是否缩放
        scale = self.scale_factor if self.hovered else 1.0
        scaled_w = int(self.rect.width * scale)
        scaled_h = int(self.rect.height * scale)
        scaled_image = pygame.transform.smoothscale(self.image, (scaled_w, scaled_h))
        # 将缩放后的图片居中于原始按钮位置
        img_rect = scaled_image.get_rect(center=self.rect.center)
        surface.blit(scaled_image, img_rect)


class PuzzleEditorUI:
    """拼图编辑器UI主类"""
    def __init__(self, main_screen, editor_logic):
        self.screen = main_screen
        self.editor_logic = editor_logic
        self.clock = pygame.time.Clock()

        # 隐藏Tkinter根窗口
        self.root = Tk()
        self.root.withdraw()

        # 加载背景图
        bg_path = "src/assets/images/editor_backgroundImage.png"
        if os.path.exists(bg_path):
            self.background_image = pygame.image.load(bg_path).convert()
            self.background_image = pygame.transform.smoothscale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            print(f"【警告】背景图未找到: {bg_path}")
            self.background_image = None

        # --- 初始化预览区 (初始尺寸) ---
        # 初始尺寸可以是最大尺寸或一个默认值
        initial_preview_size = self.editor_logic.max_preview_size  # (600, 600)
        self.preview_rect = pygame.Rect(0, 0, *initial_preview_size)  # 位置将在 update_layout 中设置
        self.preview_surface = pygame.Surface(initial_preview_size, pygame.SRCALPHA)
        self.preview_surface.fill(PIECE_BG_COLOR)

        # --- 按钮 (初始位置和尺寸) ---
        self.button_width = 250
        self.button_height = 60
        # 按钮的位置将在 update_layout 中根据最终的 preview_rect 计算

        self.buttons = []  # 按钮列表将在 update_layout 中初始化

        # 初始布局
        self.update_layout()

        # 初始绘制
        self.clear_previews()
        self.draw()

    def update_layout(self):
        """根据预览区尺寸更新布局"""
        status = self.editor_logic.get_status()
        # 获取最新的预览区尺寸
        preview_w, preview_h = status.get("preview_size", self.editor_logic.max_preview_size)

        # --- 更新预览区 Rect ---
        # 位置：居中于屏幕左侧区域 (假设屏幕宽度足够)
        margin_x = 20
        margin_y = (SCREEN_HEIGHT - preview_h) // 2
        # 确保顶部有最小边距
        margin_y = max(40, margin_y)
        self.preview_rect = pygame.Rect(margin_x, margin_y, preview_w, preview_h)
        # 更新预览 Surface
        if self.preview_surface.get_size() != (preview_w, preview_h):
            self.preview_surface = pygame.Surface((preview_w, preview_h), pygame.SRCALPHA)
            self.preview_surface.fill(PIECE_BG_COLOR)

        # --- 更新按钮位置 ---
        # 按钮区域在预览区右侧
        button_area_x = self.preview_rect.right + 20
        button_area_width = SCREEN_WIDTH - button_area_x - 20

        # 按钮居中于按钮区域
        button_x = button_area_x + (button_area_width - self.button_width) // 2

        # 按钮垂直居中 (或靠近顶部一点)
        total_button_height = 3 * self.button_height + 2 * 20  # 3个按钮 + 2个间距
        start_y = (SCREEN_HEIGHT - total_button_height) // 2
        start_y = max(100, start_y)  # 确保按钮不会太靠上

        # 重新创建按钮列表 (或更新现有按钮位置)
        button_paths = [
            "src/assets/images/buttons/import_images.png",
            "src/assets/images/buttons/set_puzzle.png",
            "src/assets/images/buttons/save_settings.png",
            "src/assets/images/buttons/return_to_menu.png"
        ]
        self.buttons = []
        for i, path in enumerate(button_paths):
            btn_y = start_y + i * (self.button_height + 20)
            self.buttons.append(Button(button_x, btn_y, self.button_width, self.button_height, path))

    def on_image_loaded(self):
        """当核心逻辑加载完图片后，UI 调用此方法更新布局"""
        print("【UI】收到图片加载完成通知，更新布局...")
        self.update_layout()
        self.update_previews()
        self.update_title()
        self.draw()


    def run(self):
        """运行编辑器主循环"""
        print("【信息】进入拼图编辑器 UI 循环...")
        pygame.display.set_caption("智慧拼图 - 拼图编辑器")
        self.update_title()

        running = True
        while running:
            running = self.handle_events()
            self.clock.tick(60)

        print("【信息】退出拼图编辑器 UI 循环...")
        pygame.display.set_caption("智慧拼图")

    def handle_events(self):
        """处理事件"""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.editor_logic.on_ui_quit()
                return False

            # 处理按钮事件
            for button in self.buttons:
                if event.type == pygame.MOUSEMOTION or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    button.handle_event(event)

                if button.handle_event(event):  # 如果返回 True 表示发生点击
                    actions_map = {
                        0: self.editor_logic.load_image_ui,
                        1: self.editor_logic.setup_puzzle_ui,
                        2: self.editor_logic.save_settings_ui,
                        3: self.editor_logic.return_to_menu,  # 调用 return_to_menu
                    }
                    action_func = actions_map.get(self.buttons.index(button))
                    if action_func:
                        action_func()  # 执行函数
                        self.update_previews()
                        self.update_title()
                        self.draw()

        # ✅ 关键修复：检查逻辑层是否要求退出
        # 如果 editor_logic.running 变为 False，则退出 UI 循环
        if not self.editor_logic.running:
            return False

        return True

    def draw(self):
        """绘制界面"""
        # 绘制背景图或纯色背景
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(BACKGROUND_COLOR)

        # 不再绘制标题文字 "拼图编辑器"

        # 绘制说明文字（使用 zhengwen.ttf, 36）
        status = self.editor_logic.get_status()
        if not status["has_image"]:
            instruction = font_size.render("请先导入图片", True, TEXT_COLOR)
            self.screen.blit(instruction, (20, self.preview_rect.bottom + 10))
        else:
            id_text = status['puzzle_id'] if status['puzzle_id'] else '未保存'
            shape_text = status['puzzle_shape']
            instruction = font_size.render(f"ID: {id_text} | 形状: {shape_text}", True, TEXT_COLOR)
            self.screen.blit(instruction, (20, self.preview_rect.bottom + 10))

        # 绘制预览区
        # pygame.draw.rect(self.screen, GRID_COLOR, self.preview_rect, 2)
        self.screen.blit(self.preview_surface, (self.preview_rect.x, self.preview_rect.y))
        preview_title = font_size.render("整体预览", True, TEXT_COLOR)
        self.screen.blit(preview_title, (self.preview_rect.x+ 120, self.preview_rect.y - 40))

        # 绘制拼图块网格（方形）
        if status["has_image"] and status["puzzle_shape"] == "方形":
            num_pieces = status["order"]
            self.draw_grid(num_pieces)

        # 绘制拼图块网格（三角形）+ 对角线
        elif status["has_image"] and status["puzzle_shape"] == "三角形":
            num_pieces = status["order"]
            piece_width = self.preview_rect.width // num_pieces
            piece_height = self.preview_rect.height // num_pieces
            self.draw_grid(num_pieces)
            for row in range(num_pieces):
                for col in range(num_pieces):
                    top_left_x = self.preview_rect.x + col * piece_width
                    top_left_y = self.preview_rect.y + row * piece_height
                    top_right_x = top_left_x + piece_width
                    bottom_left_y = top_left_y + piece_height
                    pygame.draw.line(self.screen, GRID_COLOR,
                                     (top_right_x, top_left_y),
                                     (top_left_x, bottom_left_y), 1)

        # 绘制拼图块网格（不规则）
        elif status["has_image"] and status["puzzle_shape"] == "不规则":
            # 由于无法导入 generate_jigsaw_mask，此处省略
            pass

        # 绘制按钮（无文字）
        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def clear_previews(self):
        self.preview_surface.fill(PIECE_BG_COLOR)

    def update_previews(self):
        preview_image = self.editor_logic.get_preview_image(self.preview_rect.width, self.preview_rect.height)
        if preview_image:
            self.draw_image_to_surface(preview_image, self.preview_surface)
        else:
            self.preview_surface.fill(PIECE_BG_COLOR)
        self.draw()

    def update_title(self):
        status = self.editor_logic.get_status()
        id_text = status['puzzle_id'] if status['puzzle_id'] else 'None'
        pygame.display.set_caption(f"智慧拼图 - 拼图编辑器 (ID: {id_text})")

    def draw_image_to_surface(self, image, surface):
        """将 PIL Image 绘制到 Pygame Surface"""
        surface.fill(PIECE_BG_COLOR)
        if image:
            # PIL 图像尺寸
            img_width, img_height = image.size
            surf_width, surf_height = surface.get_size()

            # 如果尺寸不匹配，进行缩放以适应 Surface (保持比例)
            if (img_width, img_height) != (surf_width, surf_height):
                # 使用 thumbnail 确保图片适应Surface且不超出
                image = image.copy()  # 避免修改原始图片
                image.thumbnail((surf_width, surf_height), Image.Resampling.LANCZOS)
                img_width, img_height = image.size  # 更新缩放后的尺寸

            # 转换为 Pygame Surface
            # --- 关键修改：统一转换为 RGBA 模式 ---
            try:
                # 将图像转换为 RGBA 模式，以兼容透明度并简化后续处理
                # convert('RGBA') 可以处理 'P', 'RGB', 'L' 等多种模式
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')

                # 此时 image.mode 应该是 'RGBA'
                mode = image.mode
                size = image.size
                data = image.tobytes()

                # 从字符串数据创建 Pygame Surface
                pygame_image = pygame.image.fromstring(data, size, mode)

                # 居中放置到 Surface 上 (如果缩放后尺寸小于Surface)
                x = (surf_width - img_width) // 2
                y = (surf_height - img_height) // 2

                # 使用 blit 将图像绘制到目标 surface 上
                # 因为 source (pygame_image) 和 dest (surface) 都是 RGBA，
                # 默认的 blit 会正确处理 alpha 通道（如果 surface 支持的话）
                surface.blit(pygame_image, (x, y))

            except Exception as e:
                print(f"【错误】将 PIL Image 转换为 Pygame Surface 时出错: {e}")
                import traceback
                traceback.print_exc()  # 打印完整的错误堆栈，便于调试
                surface.fill((255, 0, 0))  # 用红色填充表示错误
        else:
            surface.fill(PIECE_BG_COLOR)

    def draw_grid(self, num_pieces):
        piece_width = self.preview_rect.width // num_pieces
        piece_height = self.preview_rect.height // num_pieces
        for i in range(num_pieces + 1):
            x = self.preview_rect.x + i * piece_width
            y = self.preview_rect.y + i * piece_height
            pygame.draw.line(self.screen, GRID_COLOR, (x, self.preview_rect.y),
                             (x, self.preview_rect.y + self.preview_rect.height), 1)
            pygame.draw.line(self.screen, GRID_COLOR, (self.preview_rect.x, y),
                             (self.preview_rect.x + self.preview_rect.width, y), 1)