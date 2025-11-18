# src/ui/main_menu.py

import pygame
import os

# 模拟导入，因为实际导入会失败
# from utils.font_loader import load_font
# from config import SCREEN_WIDTH, SCREEN_HEIGHT

# 临时定义常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Button:
    def __init__(self, x, y, width, height, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image  # 单一图片，用于正常状态
        self.is_hovered = False
        self.scale_factor = 1.2  # 悬停时的缩放比例

    def draw(self, surface):
        if self.image:
            # 根据是否悬停决定是否缩放
            scale = self.scale_factor if self.is_hovered else 1
            scaled_width = int(self.rect.width * scale)
            scaled_height = int(self.rect.height * scale)
            scaled_image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))
            # 将缩放后的图片居中于原始按钮位置
            scaled_rect = scaled_image.get_rect(center=self.rect.center)
            surface.blit(scaled_image, scaled_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

# 获取当前文件所在目录（src/ui）
current_dir = os.path.dirname(os.path.abspath(__file__))
# 计算 assets 目录路径：src/assets
assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')

def show_main_menu(screen):
    """显示主菜单"""
    
    # 背景图路径：src/assets/images/backgroundImage_v1.png
    background_image_path = os.path.join(assets_dir, 'images', 'backgroundImage_v1.png')
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # 模拟字体加载
    font_medium = pygame.font.Font(None, 36)

    title = font_medium.render("智慧拼图", True, (0, 0, 0))
    # title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    # 按钮数据：只需提供正常状态图片名
    button_data = [
        {"image": "start_normal.png"},
        {"image": "load_normal.png"},
        {"image": "settings_normal.png"},
        {"image": "ranking_normal.png"},
        {"image": "editor_normal.png"},
        {"image": "quit_normal.png"}
    ]

    buttons = []
    y_positions = [SCREEN_HEIGHT//2-80, SCREEN_HEIGHT//2-10, SCREEN_HEIGHT//2+60,
                   SCREEN_HEIGHT//2+130, SCREEN_HEIGHT//2+200, SCREEN_HEIGHT//2+270]

    for i, data in enumerate(button_data):
        x = SCREEN_WIDTH * 0.7  # 往左移动一点
        y = y_positions[i] + 20  # 往下移动一点
        image_path = os.path.join(assets_dir, 'images', 'buttons', data["image"])
        
        # 调试：打印实际加载路径
        print(f"Loading button image: {image_path}")
        if not os.path.exists(image_path):
            print(f"⚠️ 文件不存在: {image_path}")
            button_img = None
        else:
            button_img = pygame.image.load(image_path)
        
        button = Button(x, y, 200, 50, button_img)
        buttons.append(button)

    clock = pygame.time.Clock()
    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(background_image, (0, 0))
        # 不再绘制标题文字
        # screen.blit(title, title_rect)

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            for i, btn in enumerate(buttons):
                if btn.is_clicked(event):
                    return ['start', 'load', 'settings', 'ranking', 'editor', 'quit'][i]

        pygame.display.flip()
        clock.tick(60)