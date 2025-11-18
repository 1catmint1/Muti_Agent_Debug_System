# game/game_logic.py
# 在line 298 run_puzzle_game函数中添加了BGM判断与调用的逻辑，在line 549也做了修改

import pygame
import sys
import os
import random
import pickle
import time
import json
from PIL import Image
import tkinter as tk
from tkinter import simpledialog
from utils.normalizer import normalize_shape as norm_shape_for_rank, infer_image_id
from tkinter import messagebox


from utils.font_loader import load_font

# --- 添加项目根目录到 sys.path ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- 导入配置 ---
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PIECE_AREA_HEIGHT,
    BACKGROUND_COLOR, GRID_COLOR, TEXT_COLOR, PIECE_BG_COLOR,
    SAVE_DIR, RANKING_DIR, CUSTOM_IMAGE_DIR,
    FONT_PATHS, FONT_SIZES
)

ASSETS_BASE_DIR = CUSTOM_IMAGE_DIR

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

# --- 导入组件 ---
from game.puzzle_piece import PuzzlePiece
from ui.start_screen_ui import Button, show_save_slot_selection, show_start_screen # 导入UI组件
from data.ranking_manager import RankingManager
# from ui.ranking_ui import show_ranking  # 假设存在
# from editor.puzzle_editor import PuzzleEditor  # 假设存在

# # --- 加载字体函数 ---
# def load_font(size):
#     for path in FONT_PATHS:
#         if os.path.exists(path):
#             try:
#                 return pygame.font.Font(path, size)
#             except pygame.error:
#                 continue
#     return pygame.font.SysFont(None, size)

# --- 目标区域类 ---
class TargetArea:
    def __init__(self, x, y, width, height, piece_ids, grid_x, grid_y):
        self.rect = pygame.Rect(x, y, width, height)
        self.piece_ids = piece_ids if isinstance(piece_ids, (list, tuple)) else [piece_ids]
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_pos = (grid_x, grid_y)  # 方便使用

    def contains_id(self, piece_id):
        """检查该目标区域是否接受这个 piece_id"""
        return piece_id in self.piece_ids

    def draw(self, surface):
        pygame.draw.rect(surface, GRID_COLOR, self.rect, 2)  # 边框
        from config import FONT_SIZES
        from game.game_logic import load_font
        font = load_font(max(12, FONT_SIZES['small'] // 2))
        ids_text = ",".join(map(str, self.piece_ids))
        text_surface = font.render(ids_text, True, (0, 255, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

# --- 存档管理函数 ---
def save_game_state(rows, cols, pieces_data, start_time, solved_positions, shape_type, image_path, slot=1):
    """
    保存游戏到指定槽位 (1, 2, 3)
    新增参数: shape_type - 拼图形状类型 ('jigsaw', 'triangle', 'rectangle')
    """
    # 动态bug4: 边界条件处理不当
    # 当slot参数为非数字时不会报错
    try:
        save_path = SAVE_SLOTS.get(slot)
    except TypeError:
        # 虽然捕获了异常，但没有返回值
        print(f"存档槽位类型错误: {slot}")
        # 没有返回语句，将导致函数继续执行并可能引发其他错误
    
    if not save_path:
        print(f"无效的存档槽位: {slot}")
        return False

    state = {
        'rows': rows,
        'cols': cols,
        'pieces': pieces_data,
        'start_time': start_time,
        'solved_positions': solved_positions,
        'shape_type': shape_type,
        'image_path': image_path,  
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open(save_path, 'wb') as f:
            pickle.dump(state, f)
        print(f"🎮 游戏进度已保存到存档槽 {slot}，模式: {shape_type} ({rows}x{cols})")
        return True
    except Exception as e:
        print(f"保存游戏进度到槽 {slot} 时出错: {e}")
        return False

def load_game_state(slot=1):
    save_path = SAVE_SLOTS.get(slot)
    if not save_path or not os.path.exists(save_path):
        print(f"存档槽 {slot} 不存在。")
        return None
    try:
        with open(save_path, 'rb') as f:
            state = pickle.load(f)
        print(f"📤 已从存档槽 {slot} 加载游戏进度。")
        return state
    except Exception as e:
        print(f"加载存档槽 {slot} 时出错: {e}")
        return None


def delete_save(slot):
    save_path = SAVE_SLOTS.get(slot)
    if os.path.exists(save_path):
        try:
            os.remove(save_path)
            print(f"🗑️ 已删除存档槽 {slot}")
            return True
        except OSError as e:
            print(f"删除存档 {slot} 失败: {e}")
            return False
    return False

# --- 胜利界面 ---
def show_completion_screen(screen, time_taken):
    """
    显示游戏完成界面。
    返回: 'restart', 'menu', 'quit'
    """
    font_large = load_font('zhengwen.ttf', 64)
    font_medium = load_font('zhengwen.ttf', 36)
    font_small = load_font('zhengwen.ttf', 18)

    # 加载背景图片
    background_image_path = 'src/assets/images/startScreen_backgroundImage.png'
    if os.path.exists(background_image_path):
        background_image = pygame.image.load(background_image_path).convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        print("Background image not found!")
        background_image = None

    screen.blit(background_image, (0, 0))

    congrats_text = font_large.render("恭喜完成!", True, TEXT_COLOR)
    time_text = font_medium.render(f"用时: {time_taken} 秒", True, TEXT_COLOR)

    restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "再玩一次", font_medium)
    menu_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50, "主菜单", font_medium)
    quit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 140, 200, 50, "退出游戏", font_medium)
    buttons = [restart_button, menu_button, quit_button]

    screen.blit(congrats_text, (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 4 + 60))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if restart_button.is_clicked(event):
                return 'restart'
            if menu_button.is_clicked(event):
                return 'menu'
            if quit_button.is_clicked(event):
                return 'quit'

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        pygame.display.flip()

# --- 自定义设置 ID 输入 ---
def get_id():
    root = tk.Tk()
    root.withdraw()
    user_id = simpledialog.askstring(title="输入自定义拼图设置ID", prompt="请输入ID")
    if user_id is not None:
        print(f"您输入的 ID 是: {user_id}")
    else:
        print("您取消了输入。")
    root.destroy()
    return user_id


def show_error_message(message):
    # 创建一个隐藏的主窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    root.attributes("-topmost", True)  # 尝试将弹窗置顶

    # 显示错误信息弹窗
    messagebox.showerror("拼图游戏 - 错误", message)

    # 销毁隐藏的主窗口
    root.destroy()

# --- 游戏控制类 ---
class GameController:
    def __init__(self, screen, audio_manager=None):
        self.screen = screen
        self.puzzle_id = ''
        self.puzzle_shape = 'jigsaw'
        self.puzzle_order = 3
        self.image_path = None
        self.audio_manager = audio_manager  # 保存引用

    def start_new_game(self):
        IMAGE_PATH = os.path.join("src", "assets", "nature", "dragon.jpeg")
        if not os.path.exists(IMAGE_PATH):
            print(f"错误: 找不到图像文件 '{IMAGE_PATH}'")
            return 'menu'
         # 显示难度选择界面
        rows, cols, load_saved, action, shape_style = show_start_screen(self.screen, IMAGE_PATH)
        if action == 'quit':
            return 'quit'
        elif action == 'menu':
            return 'menu'

        if action == 'play':
            slot = None
            result = run_puzzle_game(
                self.screen,
                rows, cols,
                shape_type=shape_style,
                image_path=IMAGE_PATH,
                load_saved=False,
                save_slot=slot
            )
            return result

        elif action == 'setting':
            while True:
                puzzle_id = get_id()
                if puzzle_id is None:
                    return self.start_new_game()

                image_path, puzzle_shape, puzzle_order = self.load_settings(puzzle_id)
                if image_path is not None: # 成功加载
                     result = run_puzzle_game(self.screen, puzzle_order, puzzle_order, puzzle_shape,
                                             image_path=image_path, load_saved=False, save_slot=None)
                     return result

        return 'menu'

    # game/game_logic.py - GameController.load_game()

    def load_game(self):
        slot = show_save_slot_selection(self.screen, "选择要加载的存档")
        if slot == 'back':
            return 'menu'
        if slot in [1, 2, 3]:
            state = load_game_state(slot)
            if state:
                # ✅ 从存档中获取 shape_type，默认为 'jigsaw'
                saved_shape_type = state.get('shape_type', 'jigsaw')
                print(f"📘 存档信息: {state['rows']}x{state['cols']}, 模式={saved_shape_type}, 时间={state.get('timestamp')}")

                result = run_puzzle_game(
                    self.screen,
                    state['rows'],
                    state['cols'],
                    shape_type=saved_shape_type,   
                    image_path=state.get('image_path'),               
                    load_saved=True,
                    save_slot=slot
                )
                return result
            else:
                print("加载失败，返回主菜单")
        return 'menu'

    def load_settings(self, puzzle_id):
        settings_path = os.path.join(ASSETS_BASE_DIR, puzzle_id, "settings.json")
        # font_medium = load_font(FONT_SIZES['medium']) # 用于错误提示
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            print(f"成功加载拼图设置 ID: {puzzle_id}")
            image_path = settings['image_path']
            puzzle_shape = settings['shape']
            puzzle_order = settings['order']
            return image_path, puzzle_shape, puzzle_order
        except FileNotFoundError:
            print(f"错误：未找到 ID 为 '{puzzle_id}' 的拼图设置。请检查路径 {settings_path}")
            # 在 Pygame 窗口显示错误并等待用户按键
            show_error_message(f"未找到 ID '{puzzle_id}' 的设置。")
            return None, "", 0 # 返回 None 表示失败
        except Exception as e:
            print(f"加载设置时出错: {e}")
             # 在 Pygame 窗口显示通用错误并等待用户按键
            show_error_message(f"加载 ID '{puzzle_id}' 的设置时出错。")
            return None, "", 0 # 返回 None 表示失败


# --- 游戏核心逻辑 ---
def run_puzzle_game(screen, rows, cols, shape_type, image_path=None, load_saved=False, save_slot=1):
    """
    运行拼图游戏的核心循环。
    返回: 'menu', 'restart', 'quit'
    """
    # 静态bug4: 重复定义变量
    current_dir = os.path.dirname(__file__)          # game/
    project_root = os.path.dirname(current_dir)      # 项目根目录
    
    # 重复定义
    current_dir = os.path.dirname(os.path.abspath(__file__))  # 覆盖之前的定义


    font_small = load_font('zhengwen.ttf', 18)

    # --- 正确获取项目根目录 ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.normpath(os.path.join(current_dir, '..', 'assets'))

    
    # --- 加载背景图片 ---
    bg_path = os.path.join("src/assets/images/gameBackground_v1.png")
    background_image = None
    if os.path.exists(bg_path):
        try:
            background_image = pygame.image.load(bg_path).convert()
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"加载背景图失败: {e}")

    # --- 加载音效 ---
    correct_sound = None
    sound_path = os.path.join("src", "assets", "music", "correct.wav")
    if os.path.exists(sound_path):
        try:
            correct_sound = pygame.mixer.Sound(sound_path)
        except pygame.error as e:
            print(f"加载音效失败: {e}")
    else:
        print(f"音效文件未找到: {sound_path}")

    played_sound_for = set()

    # 静态bug5: 函数内未使用的辅助函数
    def _calculate_something_complex(x, y):
        """这个函数定义了但从未被调用"""
        result = x * y
        for i in range(100):
            result += i
        return result / 2
    
    # 归一工具函数
    def _normalize_shape(shape_str: str) -> str:
        m = {
            'square': 'rectangle', 'rectangle': 'rectangle', '正方形': 'rectangle', '方形': 'rectangle',
            'triangle': 'triangle', '三角形': 'triangle',
            'irregular': 'jigsaw', 'jigsaw': 'jigsaw', '不规则': 'jigsaw', '凹凸形': 'jigsaw'
        }
        return m.get(shape_str, 'irregular')

    def _infer_image_id(image_path_: str) -> str:
        if not image_path_:
            return "default"
        parts = os.path.normpath(image_path_).split(os.sep)
        if 'custom' in parts:
            idx = parts.index('custom')
            if idx + 1 < len(parts):
                return parts[idx + 1]
        return os.path.splitext(os.path.basename(image_path_))[0]

    # 1) 图片
    if image_path is None:
        image_path = os.path.join("src", "assets", "nature", "dragon.jpeg")
        # 静态bug6: 不必要的括号
        if (not os.path.exists(image_path)):
            # 动态bug3: 条件逻辑问题，即使文件不存在也不返回
            print(f"错误: 找不到图像文件 '{image_path}'。")
            # 注释掉了返回语句，导致即使找不到文件也会继续执行
            # return 'menu'
        
    print(f"🎯 启动拼图游戏：{rows}x{cols}, 模式={shape_type}, 图片={image_path}")

    try:
        full_image = pygame.image.load(image_path).convert()
        # 计算缩略图尺寸 (例如，最大宽度150px)
        thumb_max_width = 150
        thumb_scale_factor = thumb_max_width / full_image.get_width()
        thumb_width = int(full_image.get_width() * thumb_scale_factor)
        thumb_height = int(full_image.get_height() * thumb_scale_factor)
        thumbnail_image = pygame.transform.smoothscale(full_image, (thumb_width, thumb_height))
        # 定义缩略图在屏幕上的位置 (右上角)
        thumbnail_rect = thumbnail_image.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    except Exception as e:
        print(f"加载或缩放原图失败: {e}")
        thumbnail_image = None
        thumbnail_rect = None

    # --- 2. 生成锯齿状碎片 (使用 game.generate_jigsaw_mask) ---
    shape_type = _normalize_shape(shape_type)
    print(shape_type)
    if shape_type == 'jigsaw':
        print("正在生成锯齿状拼图碎片...")
        from game.generate_jigsaw_mask import split_image_with_jigsaw_mask
        # 直接返回 Pygame Surface，不保存到文件
        original_pieces_data = split_image_with_jigsaw_mask(image_path, rows, cols, return_surfaces=True)
    elif shape_type == 'triangle':
        print("正在生成三角形拼图碎片...")
        from game.generate_triangle_mask import split_image_with_triangle_mask
        original_pieces_data = split_image_with_triangle_mask(
            image_path, rows, cols,
            return_surfaces=True,
            debug=True  # 开启调试模式，显示编号和分割线
        )
    elif shape_type == 'rectangle':
        print("正在生成矩形拼图碎片...")
        from game.generate_rectangle_mask import split_image_with_rectangle_mask
        original_pieces_data = split_image_with_rectangle_mask(image_path, rows, cols, return_surfaces=True)
    else:
        print("不支持的拼图类型。")
        return 'menu'
    if not original_pieces_data:
        print("生成碎片失败。")
        return 'menu'

     # 尝试从第一个碎片推断尺寸
    if original_pieces_data:
        example_piece = original_pieces_data[0]['image']
        piece_width = example_piece.get_width()
        piece_height = example_piece.get_height()
    else:
        print("没有生成任何碎片。")
        return 'menu'

    # 计算原始图片尺寸（用于居中显示）
    try:
        with Image.open(image_path) as img:
            original_image_width, original_image_height = img.size
    except Exception as e:
        print(f"无法使用 PIL 获取原始图片尺寸: {e}")
        # Fallback: 使用碎片尺寸估算
        original_image_width = piece_width * cols
        original_image_height = piece_height * rows

    # 计算拼图显示区域的总尺寸
    puzzle_display_width = piece_width * cols
    puzzle_display_height = piece_height * rows
    # 3) 布局偏移
    puzzle_offset_x = (SCREEN_WIDTH - puzzle_display_width) // 2
    puzzle_offset_y = (SCREEN_HEIGHT - PIECE_AREA_HEIGHT - puzzle_display_height) // 2

    # 4) 目标区域（基于原图尺寸）
    try:
        with Image.open(image_path) as img:
            original_image_width, original_image_height = img.size
    except Exception as e:
        print(f"无法读取原始图片尺寸，使用估算值: {e}")
        original_image_width = piece_width * cols
        original_image_height = piece_height * rows

    cell_width = original_image_width // cols
    cell_height = original_image_height // rows

    puzzle_display_width = original_image_width
    puzzle_display_height = original_image_height

    puzzle_offset_x = (SCREEN_WIDTH - puzzle_display_width) // 2
    puzzle_offset_y = (SCREEN_HEIGHT - PIECE_AREA_HEIGHT - puzzle_display_height) // 2

    # 收集每个格子对应的所有 piece_id
    grid_dict = {}
    for data in original_pieces_data:
        grid_x = data['col']
        grid_y = data['row']
        piece_id = data['id']
        
        key = (grid_x, grid_y)
        if key not in grid_dict:
            grid_dict[key] = []
        grid_dict[key].append(piece_id)

    # 创建目标区域
    target_areas = []
    for (grid_x, grid_y), piece_ids in grid_dict.items():
        x = puzzle_offset_x + grid_x * cell_width
        y = puzzle_offset_y + grid_y * cell_height
        area = TargetArea(x, y, cell_width, cell_height, piece_ids, grid_x, grid_y) 
        target_areas.append(area)

    # 5) 初始化拼图碎片
    puzzle_pieces = []
    start_time = time.time() if not load_saved else None
    piece_area_rect = pygame.Rect(0, SCREEN_HEIGHT - PIECE_AREA_HEIGHT, SCREEN_WIDTH, PIECE_AREA_HEIGHT)

    # 6) 底部区域布局
    total_pieces = len(original_pieces_data)
    pieces_per_row_in_area = cols
    num_rows_in_area = (total_pieces + pieces_per_row_in_area - 1) // pieces_per_row_in_area
    available_area_width = SCREEN_WIDTH - 20
    available_area_height = PIECE_AREA_HEIGHT - 20
    area_piece_width = min(piece_width, available_area_width // pieces_per_row_in_area)
    area_piece_height = min(piece_height, available_area_height // num_rows_in_area)
    piece_area_start_y = SCREEN_HEIGHT - PIECE_AREA_HEIGHT + (PIECE_AREA_HEIGHT - (num_rows_in_area * area_piece_height)) // 2

    # --- 7. 加载存档或初始化新游戏 ---
    # --- 加载存档时 ---
    if load_saved:
        saved_state = load_game_state(save_slot)
        if saved_state and saved_state['rows'] == rows and saved_state['cols'] == cols:
            print("正在恢复存档进度...")
            saved_shape = saved_state.get('shape_type', 'jigsaw')
            if saved_shape != shape_type:
                print(f"⚠️ 警告：存档模式为 {saved_shape}，但当前为 {shape_type}，可能导致显示异常！")
            start_time = saved_state.get('start_time', time.time())
            pieces_data_from_save = saved_state['pieces']
            solved_positions_from_save = saved_state.get('solved_positions', {})

            # ✅ 构建 id -> 保存数据 的字典
            saved_map = {item['id']: item for item in pieces_data_from_save}

            # ✅ 遍历原始图片数据，根据 id 查找对应的保存状态
            for data in original_pieces_data:
                piece_id = data['id']
                if piece_id in saved_map:
                    saved_data = saved_map[piece_id]
                    piece_rect_x, piece_rect_y = saved_data['rect']
                    solved = saved_data['solved']
                else:
                    # 如果没有保存数据（理论上不会发生），按新游戏处理
                    area_row = len(puzzle_pieces) // cols
                    area_col = len(puzzle_pieces) % cols
                    start_x = 10 + area_col * area_piece_width + area_piece_width // 2 - piece_width // 2
                    start_y = piece_area_start_y + area_row * area_piece_height + area_piece_height // 2 - piece_height // 2
                    piece_rect_x, piece_rect_y = start_x, start_y
                    solved = False

                piece = PuzzlePiece(
                    data['image'], data['row'], data['col'], data['id'],
                    piece_rect_x, piece_rect_y
                )
                piece.solved = solved
                puzzle_pieces.append(piece)

            print("存档恢复完成。")
            load_saved = True


    if not load_saved:
        start_time = time.time()

        # 创建索引列表并打乱
        indices = list(range(len(original_pieces_data)))
        random.shuffle(indices)  # 打乱顺序

        for idx, original_idx in enumerate(indices):
            data = original_pieces_data[original_idx]

            area_row = idx // pieces_per_row_in_area
            area_col = idx % pieces_per_row_in_area
            start_x = 10 + area_col * area_piece_width + area_piece_width // 2 - piece_width // 2
            start_y = piece_area_start_y + area_row * area_piece_height + area_piece_height // 2 - piece_height // 2

            piece = PuzzlePiece(
                data['image'], data['row'], data['col'], data['id'],
                start_x, start_y
            )
            piece.solved = False
            puzzle_pieces.append(piece)

    # 8) 存档辅助
    def get_pieces_save_data(pieces):
        return [{'id': p.id, 'rect': (p.rect.x, p.rect.y), 'solved': p.solved} for p in pieces]

    def get_solved_positions(pieces, target_areas_):
        solved_map = {}
        for piece in pieces:
            if piece.solved:
                center_point = piece.rect.center
                for area in target_areas_:
                    if area.rect.collidepoint(center_point):
                        solved_map[area.grid_pos] = piece.id
                        break
        return solved_map

    # 9) 游戏主循环
    clock = pygame.time.Clock()
    running = True

    # --- 添加保存按钮 ---
    font_small = load_font('zhengwen.ttf', 18)
    #save_button = Button(SCREEN_WIDTH - 120, 10, 100, 40, "保存游戏", font_small)
    save_img = os.path.join("assets", 'images', 'buttons', "save.png")
    #save_img = pygame.transform.scale(btn_w, btn_h)
    return_img = os.path.join("assets", 'images', 'buttons', "return_to_menu.png")
    #return_img = pygame.transform.scale(btn_w, btn_h)

    # save_img = os.path.join("src/assets/images/buttons/save.png")
    # return_img = os.path.join("src/assets/images/buttons/return_to_menu.png")

    # 设置按钮大小（像素）。如需与图片原始尺寸一致，可用 pygame.image.load 后读取尺寸。
    btn_w, btn_h = 150, 80


    # 将保存按钮放在左上角计时器下方
    save_btn_x = 10
    save_btn_y = 50 + font_small.get_height() + 8
    save_button = Button(save_btn_x, save_btn_y, btn_w, btn_h, text=None, font=None, image=save_img, scale_factor=1.2)


    # 返回按钮放在保存按钮下方
    return_btn_x = save_btn_x
    return_btn_y = save_btn_y + btn_h + 8
    return_button = Button(return_btn_x, return_btn_y, btn_w, btn_h, text=None, font=None, image=return_img, scale_factor=1.2)

    def _autosave_or_prompt():
        """用于 ESC/窗口关闭时保存：优先用当前 save_slot；否则弹出槽位选择。"""
        nonlocal save_slot
        if save_slot in [1, 2, 3]:
            save_game_state(rows, cols,
                            get_pieces_save_data(puzzle_pieces),
                            start_time,
                            get_solved_positions(puzzle_pieces, target_areas),
                            shape_type=shape_type,  # ✅ 添加
                            image_path = image_path,
                            slot=save_slot)
        else:
            selected_slot = show_save_slot_selection(screen, "选择保存位置")
            if selected_slot in [1, 2, 3]:
                save_slot = selected_slot
                save_game_state(rows, cols,
                                get_pieces_save_data(puzzle_pieces),
                                start_time,
                                get_solved_positions(puzzle_pieces, target_areas),
                                shape_type=shape_type,  # ✅ 添加
                                image_path = image_path,
                                slot=save_slot)

    def show_full_image(image_path):
        try:
            img = Image.open(image_path)
            img.show(title="拼图原图")
        except Exception as e:
            print(f"无法显示原图: {e}")

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _autosave_or_prompt()
                return 'quit'

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                _autosave_or_prompt()
                return 'menu'

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if save_button.is_clicked(event):
                    selected_slot = show_save_slot_selection(screen, "选择保存位置")
                    if selected_slot in [1, 2, 3]:
                        success = save_game_state(
                            rows, cols,
                            get_pieces_save_data(puzzle_pieces),
                            start_time,
                            get_solved_positions(puzzle_pieces, target_areas),
                            shape_type=shape_type,  
                            image_path=image_path, 
                            slot=selected_slot
                        )
                        if success:
                            # 显示保存成功提示
                            tip_font = load_font('zhengwen.ttf', 18)
                            tip_text = tip_font.render(f"已保存到槽 {selected_slot}", True, (0, 255, 0))
                            tip_rect = tip_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
                            screen.blit(tip_text, tip_rect)
                            pygame.display.flip()
                            pygame.time.delay(1000)  # 显示1秒
                        else:
                            print(f"保存失败")
                    # 如果返回 'back' 或 'quit'，则不保存，返回游戏
                    continue  # 避免触发拼图点击
                elif return_button.is_clicked(event):
                    # 直接返回主菜单（不自动保存），控制器会在 main.py 中收到 'menu'
                    return 'menu'
                # --- 检查缩略图点击 ---
                elif thumbnail_rect and thumbnail_rect.collidepoint(event.pos):
                    print("缩略图被点击，尝试显示原图...")
                    show_full_image(image_path)  # 调用显示原图函数

                # 碎片拖拽
                for piece in reversed(puzzle_pieces):
                    if piece.rect.collidepoint(event.pos) and not piece.solved:
                        puzzle_pieces.remove(piece)
                        puzzle_pieces.append(piece)
                        piece.start_drag(event.pos[0], event.pos[1])
                        break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for piece in puzzle_pieces:
                    if piece.dragging:
                        piece.stop_drag(target_areas, piece_area_rect)

            elif event.type == pygame.MOUSEMOTION:
                for piece in puzzle_pieces:
                    piece.update_position(event.pos[0], event.pos[1])

        for piece in puzzle_pieces:
            if piece.solved and piece.id not in played_sound_for:
                if correct_sound:
                    correct_sound.play()
                played_sound_for.add(piece.id)
        # --- 绘制 ---
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)
        # 绘制底部碎片区域背景
        pygame.draw.rect(screen, PIECE_BG_COLOR, piece_area_rect)
        pygame.draw.line(screen, GRID_COLOR, (0, SCREEN_HEIGHT - PIECE_AREA_HEIGHT),
                         (SCREEN_WIDTH, SCREEN_HEIGHT - PIECE_AREA_HEIGHT), 2)

        if target_areas:
            min_x = min(area.rect.x for area in target_areas)
            min_y = min(area.rect.y for area in target_areas)
            max_x = max(area.rect.right for area in target_areas)
            max_y = max(area.rect.bottom for area in target_areas)
            outline_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
            pygame.draw.rect(screen, (0, 255, 0), outline_rect, width=3)

        dragging_piece = None
        for piece in puzzle_pieces:
            if piece.dragging:
                dragging_piece = piece
            else:
                in_piece_area = piece.rect.colliderect(piece_area_rect)
                piece.draw(screen, in_piece_area=in_piece_area)
        if dragging_piece:
            in_piece_area = dragging_piece.rect.colliderect(piece_area_rect)
            dragging_piece.draw(screen, in_piece_area=in_piece_area)

        elapsed_time = int(time.time() - start_time) if start_time else 0
        time_text = font_small.render(f"时间: {elapsed_time}s", True, TEXT_COLOR)
        screen.blit(time_text, (10, 10))

        save_button.draw(screen)
        save_button.check_hover(mouse_pos)
        return_button.draw(screen)
        return_button.check_hover(mouse_pos)

        # --- 绘制缩略图 ---
        if thumbnail_image and thumbnail_rect:
            screen.blit(thumbnail_image, thumbnail_rect)
            # 可选：给缩略图加个边框
            pygame.draw.rect(screen, (200, 200, 200), thumbnail_rect, 2)

        pygame.display.flip()
        clock.tick(60)

        # 胜利判定（写入排行榜 + 胜利界面）
        if all(p.solved for p in puzzle_pieces):
            end_time = time.time()
            total_time = int(end_time - start_time)

            try:
                image_id = _infer_image_id(image_path)
                normalized_shape = _normalize_shape(shape_type)
                difficulty = int(rows)

                print("🎯 WIN detected ->",
                      f"image={image_id}, diff={difficulty}, shape={normalized_shape}, elapsed={total_time}s")

                RankingManager().add_record(
                    image=image_id,
                    difficulty=difficulty,
                    shape=normalized_shape,
                    elapsed_sec=total_time
                )
            except Exception as e:
                print(f"⚠️ 写入排行榜失败（不影响游戏流程）: {e}")

            result = show_completion_screen(screen, total_time)

            if result == 'restart':
                # 再玩一次：清理当前槽位的存档（保持你原来的行为）
                if save_slot in [1, 2, 3]:
                    delete_save(save_slot)
                return 'restart'
            elif result == 'menu':
                return 'menu'
            elif result == 'quit':
                return 'quit'
