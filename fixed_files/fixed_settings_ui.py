# src/ui/settings_ui.py

import pygame
import os
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from utils.font_loader import load_font  # ✅ 导入字体加载器

# 获取项目根目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')

# --- Slider 类（保持不变）---
class Slider:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.volume = 0.8
        self.dragging = False

    def draw(self, screen, font):
        pygame.draw.rect(screen, (150, 150, 150), self.rect, border_radius=6)
        fill_width = int(self.rect.width * self.volume)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, (100, 200, 255), fill_rect, border_radius=6)

        handle_x = self.rect.x + int(self.rect.width * self.volume)
        pygame.draw.circle(screen, (255, 255, 255), (handle_x, self.rect.centery), 10)
        pygame.draw.circle(screen, (80, 80, 80), (handle_x, self.rect.centery), 6)

        volume_text = font.render(f"{int(self.volume * 100)}%", True, (0, 0, 0))
        screen.blit(volume_text, (handle_x - volume_text.get_width() // 2, self.rect.bottom + 10))

    def check_click(self, pos):
        handle_x = self.rect.x + int(self.rect.width * self.volume)
        if abs(pos[0] - handle_x) <= 15 and abs(pos[1] - self.rect.centery) <= 15:
            self.dragging = True
            return True
        elif self.rect.collidepoint(pos):
            self.volume = (pos[0] - self.rect.x) / self.rect.width
            self.volume = max(0.0, min(1.0, self.volume))
            return True
        return False

    def update(self, mouse_x):
        if self.dragging:
            self.volume = (mouse_x - self.rect.x) / self.rect.width
            self.volume = max(0.0, min(1.0, self.volume))
            return True
        return False

    def release(self):
        self.dragging = False


def show_settings(screen, audio_manager=None):
    """
    显示设置界面：带标题、音量标签、图片按钮
    """

    # --- 加载背景图 ---
    bg_path = os.path.join(assets_dir, 'images', 'settings_backgroundImage.png')
    try:
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    except pygame.error as e:
        print(f"❌ 背景图加载失败: {bg_path}, 错误: {e}")
        background = pygame.Surface(screen.get_size())
        background.fill((40, 44, 52))

    # --- 字体加载（使用 load_font）---
    title_font = load_font('zhengwen.ttf', 64)        # 标题字体
    label_font = load_font('zhengwen.ttf', 36)         # 音量标签
    slider_font = load_font('zhengwen.ttf', 32)        # 滑块百分比

    # --- 初始化滑动条 ---
    slider = Slider(300, 300, 300, 12)
    if audio_manager:
        slider.volume = audio_manager.music_volume  # 同步当前音量

    # --- 加载返回按钮图片 ---
    button_img_path = os.path.join(assets_dir, 'images', 'buttons', 'return_to_menu.png')
    try:
        back_button_image = pygame.image.load(button_img_path).convert_alpha()
        back_button_image = pygame.transform.smoothscale(back_button_image, (200, 60))
        back_rect = back_button_image.get_rect(center=(SCREEN_WIDTH // 2, 450))
    except pygame.error as e:
        print(f"❌ 返回按钮图片加载失败: {button_img_path}, 错误: {e}")
        # 备用方案：绘制纯色按钮
        back_button_image = None
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 60)

    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        # --- 绘制标题 "设置" ---
        title_surf = title_font.render("设 置", True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        # --- 绘制左侧文本 "音量：" ---
        volume_label = label_font.render("音量：", True, (0, 0, 0))
        screen.blit(volume_label, (volume_label.get_width() - 40, 290))  # 微调位置对齐滑块

        # --- 绘制滑动条 ---
        slider.update(mouse_pos[0])
        slider.draw(screen, slider_font)

        # --- 更新音频音量 ---
        if audio_manager:
            audio_manager.set_music_volume(slider.volume)

        # --- 绘制返回按钮（优先使用图片）---
        if back_button_image:
            # 缩放判断是否悬停
            scale = 1.1 if back_rect.collidepoint(mouse_pos) else 1.0
            scaled_w = int(200 * scale)
            scaled_h = int(60 * scale)
            scaled_img = pygame.transform.smoothscale(back_button_image, (scaled_w, scaled_h))
            scaled_rect = scaled_img.get_rect(center=back_rect.center)
            screen.blit(scaled_img, scaled_rect)
        else:
            # 备用按钮样式
            color = (100, 100, 100) if back_rect.collidepoint(mouse_pos) else (130, 130, 130)
            pygame.draw.rect(screen, color, back_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 200), back_rect, 3, border_radius=10)
            fallback_text = label_font.render("返回", True, (255, 255, 255))
            screen.blit(fallback_text, fallback_text.get_rect(center=back_rect.center))

        # --- 事件处理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return 'menu'
                else:
                    slider.check_click(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                slider.release()

            if event.type == pygame.MOUSEMOTION:
                if slider.dragging:
                    slider.update(event.pos[0])

        pygame.display.flip()
        clock.tick(60)

    return 'menu'