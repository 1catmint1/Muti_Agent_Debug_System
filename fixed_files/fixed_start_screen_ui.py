# ui/start_screen_ui.py

import pygame
import sys
import os
import pickle

# --- 添加项目根目录到 sys.path ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- 导入配置 ---
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PIECE_AREA_HEIGHT,
    BACKGROUND_COLOR, GRID_COLOR, TEXT_COLOR,
    SAVE_DIR, RANKING_DIR, CUSTOM_IMAGE_DIR,
    FONT_PATHS, FONT_SIZES
)

# --- 确保必要的目录存在 ---
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(RANKING_DIR, exist_ok=True)
os.makedirs(CUSTOM_IMAGE_DIR, exist_ok=True)

# --- 定义多个存档文件路径 ---
SAVE_SLOTS = {
    1: os.path.join(SAVE_DIR, "save1.pkl"),
    2: os.path.join(SAVE_DIR, "save2.pkl"),
    3: os.path.join(SAVE_DIR, "save3.pkl")
}

# --- 按钮类 ---
class Button:
    def __init__(self, x, y, width, height, text=None, font=None, image=None, scale_factor=1.0):
        """
        支持两种按钮：
        - image: 提供图片路径或 pygame.Surface -> 显示图片（hover 时可放大）
        - 不提供 image -> 绘制矩形+文字（灰色）
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = (180, 180, 180)
        self.hover_color = (150, 150, 150)
        self.text_color = TEXT_COLOR
        self.is_hovered = False
        self.scale_factor = scale_factor

        # 图片相关
        self.image_path = image
        self.image_surf = None      # 常规尺寸的图片 Surface（与 rect 大小一致）
        self.hover_surf = None      # hover 时用的放大 Surface（如果 scale_factor != 1）

        if image:
            try:
                # 支持直接传 Surface 或 传路径字符串
                if isinstance(image, pygame.Surface):
                    loaded = image
                else:
                    # 如果是相对路径，尽量以项目为基准加载
                    img_path = image
                    if not os.path.isabs(img_path):
                        try:
                            img_path = os.path.join(project_root, img_path)
                        except Exception:
                            pass
                    loaded = pygame.image.load(img_path).convert_alpha()

                # 准备常规尺寸表面（与 rect 一致）
                self.image_surf = pygame.transform.smoothscale(loaded, (self.rect.width, self.rect.height))

                # 准备 hover 表面（如果需要放大）
                if self.scale_factor != 1.0:
                    w = max(1, int(self.rect.width * self.scale_factor))
                    h = max(1, int(self.rect.height * self.scale_factor))
                    self.hover_surf = pygame.transform.smoothscale(loaded, (w, h))
                else:
                    self.hover_surf = self.image_surf

                # debug 可选：取消下面注释查看加载信息
                # print(f"[DEBUG] 按钮图片加载成功: {image}")
            except Exception as e:
                print(f"[DEBUG] 按钮图片加载失败: {image} -> {e}")
                self.image_surf = None
                self.hover_surf = None

    def draw(self, surface):
        """
        绘制按钮：
        - 如果有图片：始终先绘制图片（非 hover 时绘制常规尺寸，hover 时绘制 hover_surf）
        - 如果没有图片：绘制矩形 + 文字（hover 切换颜色）
        """
        if self.image_surf:
            # 有图片：正常显示图片（hover 时显示放大图片，且居中）
            if self.is_hovered and self.hover_surf is not None and self.hover_surf is not self.image_surf:
                hw, hh = self.hover_surf.get_size()
                surface.blit(self.hover_surf, (self.rect.centerx - hw // 2, self.rect.centery - hh // 2))
            else:
                # 直接把预先缩放好的 image_surf blit 到 rect（不会遮盖背景）
                surface.blit(self.image_surf, self.rect)
        else:
            # 没有图片：画一个矩形 + 文字
            color = self.hover_color if self.is_hovered else self.color
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            if self.text and self.font:
                text_surf = self.font.render(self.text, True, self.text_color)
                surface.blit(
                    text_surf,
                    (self.rect.centerx - text_surf.get_width() // 2,
                     self.rect.centery - text_surf.get_height() // 2)
                )

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


# --- 存档管理函数 ---
def get_save_info(slot):
    """
    获取某个存档的基本信息（用于显示在UI上）
    """
    save_path = SAVE_SLOTS.get(slot)
    if os.path.exists(save_path):
        try:
            with open(save_path, 'rb') as f:
                state = pickle.load(f)
            return {
                'exists': True,
                'rows': state['rows'],
                'cols': state['cols'],
                'timestamp': state.get('timestamp', '未知时间'),
                'game_mode': state.get('game_mode', '未知模式')  
            }
        except Exception:
            return {'exists': False}
    return {'exists': False}

def delete_save(slot):
    save_path = SAVE_SLOTS.get(slot)
    if save_path and os.path.exists(save_path):
        try:
            os.remove(save_path)
            print(f"Deleted save slot {slot}")
            return True
        except OSError as e:
            print(f"Failed to delete save {slot}: {e}")
            return False
    return False

def show_save_slot_selection(screen, title="选择存档槽"):
    """
    显示存档槽选择界面，包含加载和删除按钮。
    返回: 'quit', 'back', 或 1, 2, 3 (表示加载的槽位)
    """
    font_large = pygame.font.SysFont(None, 64)
    font_small = pygame.font.SysFont(None, 16)
    font_medium = pygame.font.SysFont(None, 36)

    # 加载背景图片
    background_image_path = 'src/assets/images/startScreen_backgroundImage.png'
    if os.path.exists(background_image_path):
        background_image = pygame.image.load(background_image_path).convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        print("Background image not found!")
        background_image = None

    screen.blit(background_image, (0, 0))


    #screen.fill(BACKGROUND_COLOR)
    title_text = font_large.render(title, True, TEXT_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 80))

    # 存储所有按钮的列表 (按钮对象, 关联的操作或槽位)
    buttons = [] 
    # 存储删除按钮，方便单独处理
    delete_buttons = {}

    y_start = 150
    y_spacing = 70
    slot_button_width = 300
    slot_button_x = SCREEN_WIDTH // 2 - slot_button_width // 2
    delete_button_width = 80
    delete_button_x = slot_button_x + slot_button_width + 20 # 删除按钮在槽位按钮右侧

    for i in range(1, 4):
        info = get_save_info(i) # 确保 get_save_info 函数可用
        if info['exists']:
            text = f"存档 {i}: {info['rows']}x{info['cols']}  {info['timestamp']}"
        else:
            text = f"存档 {i}: 空"
        
        # 创建加载/选择存档的按钮
        slot_btn = Button(slot_button_x, y_start + i * y_spacing, slot_button_width, 50, text, font_small)
        buttons.append((slot_btn, i))
        
        # 如果存档存在，创建对应的删除按钮
        if info['exists']:
             del_btn = Button(delete_button_x, y_start + i * y_spacing, delete_button_width, 50, "删除", font_small)
             buttons.append((del_btn, f"del_{i}")) # 使用特殊标识符
             delete_buttons[i] = del_btn # 也可以用字典映射

    back_button = Button(SCREEN_WIDTH // 2 - 100, 500, 200, 50, "返回", font_medium)
    buttons.append((back_button, 'back'))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return 'quit'  

            # --- 检查所有按钮的点击 ---
            for btn, action in buttons:
                btn.check_hover(mouse_pos)
                if btn.is_clicked(event):
                    if action == 'back':
                        return 'back'
                    elif isinstance(action, int): # 加载存档
                        return action 
                    elif isinstance(action, str) and action.startswith("del_"): # 删除存档
                        slot_to_delete = int(action.split("_")[1])
                        # 调用删除函数 (确保 delete_save 可用)
                        if delete_save(slot_to_delete): 
                            print(f"存档 {slot_to_delete} 已删除。")
                            # 重新加载界面以更新显示
                            return show_save_slot_selection(screen, title) # 递归调用自身刷新
                        else:
                            print(f"删除存档 {slot_to_delete} 失败。")
                        # 如果不希望递归刷新，可以在这里重新生成按钮列表和信息
                        # 但递归刷新更简单直接
                        
        # --- 绘制 ---
        #screen.fill(BACKGROUND_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 80))
        for btn, _ in buttons:
            btn.draw(screen)
        pygame.display.flip()

    # 不建议走到这里
    return 'back'


# --- 开始界面（第二部分）---
def show_start_screen(screen, audio_manager=None):
    """
    显示游戏开始前的难度和模式选择界面。
    返回: rows, cols, False, 'play' 或 None, None, False, 'menu'/'quit'
    """

    # 加载背景图片
    background_image_path = 'src/assets/images/startScreen_backgroundImage.png'
    if os.path.exists(background_image_path):
        background_image = pygame.image.load(background_image_path).convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        print("Background image not found!")
        background_image = None

    screen.blit(background_image, (0, 0))

    font_large = pygame.font.SysFont(None, 64)
    font_medium = pygame.font.SysFont(None, 36)

    #screen.fill(BACKGROUND_COLOR)
    title_text = font_large.render("智慧拼图", True, TEXT_COLOR)

    # 难度级别列表
    difficulties = ["3x3 难度", "4x4 难度", "5x5 难度"]
    current_difficulty_index = 0

    left_button = Button(SCREEN_WIDTH // 2 - 170 - 80, SCREEN_HEIGHT // 2 - 75, 80, 50, "<", font_medium)
    right_button = Button(SCREEN_WIDTH // 2 + 170, SCREEN_HEIGHT // 2 - 75, 80, 50, ">", font_medium)

    # 模式选择列表 (当前UI未完全实现模式切换逻辑)
    styles = ["三角形", "正方形", "凹凸形"]
    current_style_index = 2

    left_button_style = Button(SCREEN_WIDTH // 2 - 170 - 80, SCREEN_HEIGHT // 2 + 10, 80, 50, "<", font_medium)
    right_button_style = Button(SCREEN_WIDTH // 2 + 170, SCREEN_HEIGHT // 2 + 10, 80, 50, ">", font_medium)

    start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 110, 200, 50, "开始游戏", font_medium)
    quit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 180, 200, 50, "返回菜单", font_medium)
    setting_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 250, 200, 50, "自定义拼图", font_medium)

    buttons = [left_button, right_button, left_button_style, right_button_style, start_button, quit_button, setting_button]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None, False, 'quit'
            # 难度选择
            if left_button.is_clicked(event) and current_difficulty_index > 0:
                current_difficulty_index -= 1
            if right_button.is_clicked(event) and current_difficulty_index < len(difficulties) - 1:
                current_difficulty_index += 1
            # 模式选择 (当前UI未完全实现模式切换逻辑)
            if left_button_style.is_clicked(event) and current_style_index > 0:
                current_style_index -= 1
            if right_button_style.is_clicked(event) and current_style_index < len(styles) - 1:
                current_style_index += 1

            if start_button.is_clicked(event):
                rows, cols = map(int, (difficulties[current_difficulty_index].split(' ')[0]).split('x'))
                if current_style_index == 0:
                    return rows, cols, False, 'play', 'triangle'
                elif current_style_index == 1:
                    return rows, cols, False, 'play', 'rectangle'
                else:
                    return rows, cols, False, 'play', 'jigsaw'
                
            if quit_button.is_clicked(event):
                return None, None, False, 'menu', None
            if setting_button.is_clicked(event):
                return None, None, False, 'setting', None
            
        screen.blit(background_image, (0, 0))

        #screen.fill(BACKGROUND_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 8))

        # 显示当前选择的难度
        selected_difficulty_text = font_medium.render(f"选择: {difficulties[current_difficulty_index]}", True, TEXT_COLOR)
        screen.blit(selected_difficulty_text, (SCREEN_WIDTH // 2 - selected_difficulty_text.get_width() // 2, SCREEN_HEIGHT // 2 - 70))

        # 显示当前选择的模式 (当前UI未完全实现模式切换逻辑)
        selected_style_text = font_medium.render(f"选择: {styles[current_style_index]}", True, TEXT_COLOR)
        screen.blit(selected_style_text, (SCREEN_WIDTH // 2 - selected_style_text.get_width() // 2, SCREEN_HEIGHT // 2 + 15))

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()

    # 理论上不会走到这里
    return None, None, False, 'menu'