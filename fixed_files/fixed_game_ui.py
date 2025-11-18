import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import os

# 获取当前文件所在目录（src/ui）
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')


class Button:
    """通用按钮类，支持图片悬停缩放"""
    def __init__(self, x, y, width, height, image=None, scale_factor=1.2):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.is_hovered = False
        self.scale_factor = scale_factor

    def draw(self, surface):
        if self.image:
            scale = self.scale_factor if self.is_hovered else 1
            scaled_width = int(self.rect.width * scale)
            scaled_height = int(self.rect.height * scale)
            scaled_image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))
            scaled_rect = scaled_image.get_rect(center=self.rect.center)
            surface.blit(scaled_image, scaled_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class GameUI:
    def __init__(self, screen):
        self.font_small = pygame.font.Font(None, 40)
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)

        # 按钮配置
        button_width, button_height = 150, 40
        self.button_spacing = 20
        self.start_y = 150  # 起始 Y 位置（避开顶部信息）
        self.x_offset = 40  # 按钮居中于左侧区域

        # 加载按钮图片（只加载 normal 状态）
        self.btn_gameSettings_img = self.load_button_image('gameSettings_normal.png')
        self.btn_home_img = self.load_button_image('home_normal.png')
        self.btn_hint_img = self.load_button_image('hint_normal.png')
        self.btn_restart_img = self.load_button_image('restart_normal.png')

        # 创建按钮实例（位置将在 draw 时更新）
        self.btn_gameSettings = Button(0, 0, button_width, button_height, self.btn_gameSettings_img, scale_factor=1.2)
        self.btn_home = Button(0, 0, button_width, button_height, self.btn_home_img, scale_factor=1.2)
        self.btn_hint = Button(0, 0, button_width, button_height, self.btn_hint_img, scale_factor=1.2)
        self.btn_restart = Button(0, 0, button_width, button_height, self.btn_restart_img, scale_factor=1.2)

        self.buttons = [
            self.btn_gameSettings,
            self.btn_home,
            self.btn_hint,
            self.btn_restart
        ]

    def load_button_image(self, filename):
        """安全加载按钮图片"""
        image_path = os.path.join(assets_dir, 'images', 'buttons', filename)
        if os.path.exists(image_path):
            return pygame.image.load(image_path).convert_alpha()
        else:
            print(f"⚠️ 按钮图片未找到: {image_path}")
            # 返回一个占位图（红色方块）
            placeholder = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (255, 0, 0), (5, 5, 50, 50))
            return placeholder

    def draw_game_screen(self, screen, pieces, target_areas, original_image, time_elapsed, moves, callbacks=None):
        """
        主游戏界面绘制
        callbacks: {'gameSettings': func, 'home': func, 'hint': func, 'restart': func}
        使用位于'src/assets/images/gameBackground_v1.png'的背景图，并调整其大小以适应屏幕尺寸。
        """
        if callbacks is None:
            callbacks = {}

        # 获取屏幕尺寸
        screen_width, screen_height = screen.get_size()

        # 加载背景图片
        background_image_path = os.path.join(assets_dir, 'images', 'gameBackground_v1.png')

        # 先检查文件是否存在
        if not os.path.exists(background_image_path):
            print(f"❌ 背景图片未找到: {background_image_path}")
            print(f"🔍 当前工作目录: {os.getcwd()}")
            print(f"📦 assets_dir 路径: {assets_dir}")
            screen.fill((0, 220, 220))  # 蓝色背景表示错误
        else:
            try:
                bg_surface = pygame.image.load(background_image_path)
                # 额外检查是否真的加载成功
                if bg_surface.get_size() == (0, 0):
                    raise ValueError("图像为空")
                # 缩放并绘制
                background_image = pygame.transform.scale(bg_surface, (screen_width, screen_height))
                screen.blit(background_image, (0, 0))
                print(f"✅ 成功加载背景图: {background_image_path}")  # 调试用，可删
            except Exception as e:
                print(f"⚠️ 加载背景图片失败: {e}")
                screen.fill((0, 220, 220))

        # === 游戏主区域绘制 ===
        piece_area_rect = pygame.Rect(0, screen.get_height() - 200, screen.get_width(), 200)
        pygame.draw.rect(screen, (240, 240, 240), piece_area_rect)
        pygame.draw.line(screen, (100, 100, 100), (0, piece_area_rect.y), (screen.get_width(), piece_area_rect.y), 2)

        for area in target_areas:
            pygame.draw.rect(screen, (100, 100, 100), area['rect'], 2)

        dragging = None
        for p in pieces:
            if p.dragging:
                dragging = p
            else:
                in_area = p.rect.colliderect(piece_area_rect)
                p.draw(screen, in_area)

        if dragging:
            in_area = dragging.rect.colliderect(piece_area_rect)
            dragging.draw(screen, in_area)

        # === 左上角信息 ===
        time_text = self.font_small.render(f"时间: {time_elapsed}s", True, (0, 0, 0))
        tip_text1 = self.font_small.render("←→: 旋转  ↑↓: 镜像", True, (0, 0, 0))
        screen.blit(tip_text1, (10, 30))

        # move_text = self.font_small.render(f"步数: {moves}", True, (0, 0, 0))
        screen.blit(time_text, (10, 10))
        # screen.blit(move_text, (10, 50))

        # === 右上角缩略图 ===
        if original_image:
            thumb = pygame.transform.smoothscale(original_image, (100, 100))
            screen.blit(thumb, (screen.get_width() - 110, 10))

        # === 左侧悬浮按钮组 ===
        self._position_buttons(screen)  # 动态定位按钮
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()

        # 事件处理（建议在主循环中做，但这里提供参考）
        self.handle_button_clicks(callbacks)

    def _position_buttons(self, screen):
        """动态设置按钮位置，确保适配屏幕"""
        for i, button in enumerate(self.buttons):
            y = self.start_y + i * (button.rect.height + self.button_spacing)
            button.rect.x = self.x_offset
            button.rect.y = y

    def handle_button_clicks(self, callbacks=None):
        """处理按钮点击事件（可由主循环调用）"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.event.post(event)  # 重新放回事件队列
                return

            for button, key in zip(self.buttons, ['gameSettings', 'home', 'hint', 'restart']):
                if button.is_clicked(event):
                    # 如果有回调就执行（保持兼容性）
                    if callbacks and key in callbacks:
                        callbacks[key]()
                    # 返回按钮名称，让控制器决定后续行为
                    return key  # 例如返回 'home'
                
        return None

    def show_completion_screen(self, screen, total_time):
        congrats = self.font_large.render("🎉 恭喜完成！", True, (0, 0, 0))
        time_text = self.font_medium.render(f"用时: {total_time} 秒", True, (0, 0, 0))
        screen.blit(congrats, (screen.get_width()//2 - congrats.get_width()//2, screen.get_height()//3))
        screen.blit(time_text, (screen.get_width()//2 - time_text.get_width()//2, screen.get_height()//3 + 60))
        pygame.display.flip()
        pygame.time.wait(2000)