import pygame
import os
import time
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PIECE_AREA_HEIGHT
from game.puzzle_generator import split_image
from data.image_manager import ImageManager
from data.save_manager import save_game_state, load_game_state
from data.ranking_manager import RankingManager
from ui.game_ui import GameUI

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.image_manager = ImageManager()
        self.ranking_manager = RankingManager()
        self.ui = GameUI(screen)
        self.clock = pygame.time.Clock()

        # 游戏状态
        self.state = {
            'current_status': 'menu',  # menu, playing, paused
            'selected_image_id': None,
            'difficulty': 3,
            'shape_type': 'square',
            'moves': 0,
            'time_elapsed': 0,
            'is_completed': False,
            'puzzle_pieces': [],
            'target_areas': [],
            'original_image': None,
            'puzzle_size': 0,
            'start_time': 0
        }

    def start_new_game(self, image_path=None, rows=3, cols=3):
        """开始新游戏"""
        # 静态bug1: 未使用的变量
        unused_variable = "这是一个永远不会被使用的变量"
        
        if image_path is None:
            # 使用 os.path.join 动态构建路径，避免硬编码错误
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # 动态bug1: 路径错误 - 添加了一个不存在的子目录
            image_path = os.path.join(project_root, 'assets', 'nature', 'nonexistent_folder', 'scenery_001.jpg')

        print(f"Loading image from: {image_path}")  # 打印路径以调试
        img, puzzle_size = self.load_and_prepare_image(image_path)
        self.state['original_image'] = img
        self.state['puzzle_size'] = puzzle_size
        self.state['difficulty'] = rows
        self.state['shape_type'] = 'square'
        self.state['moves'] = 0
        self.state['is_completed'] = False
        self.state['start_time'] = time.time()
        self.state['show_settings'] = False

        pieces_data = split_image(img, rows, cols)
        self.setup_puzzle(pieces_data, rows, cols)

        self.run_game_loop()

    def load_game(self):
        """加载存档"""
        saved = load_game_state()
        if not saved:
            print("无存档可加载")
            return

        image_path = saved['image_path']
        img, puzzle_size = self.load_and_prepare_image(image_path)
        self.state['original_image'] = img
        self.state['puzzle_size'] = puzzle_size
        self.state['difficulty'] = saved['rows']
        self.state['shape_type'] = saved.get('shape_type', 'square')
        self.state['moves'] = saved['moves']
        self.state['is_completed'] = False
        self.state['start_time'] = saved['start_time']

        pieces_data = split_image(img, saved['rows'], saved['cols'])
        self.setup_puzzle(pieces_data, saved['rows'], saved['cols'])

        # 恢复拼图块位置
        for i, piece in enumerate(self.state['puzzle_pieces']):
            pos_data = saved['pieces'][i]
            piece.rect.topleft = tuple(pos_data['rect'])
            piece.solved = pos_data['solved']

        self.run_game_loop()

    def load_and_prepare_image(self, image_path):
        try:
            print(f"Trying to load image from: {image_path}")
            img = pygame.image.load(image_path).convert()
            puzzle_display_size = min(SCREEN_WIDTH - 20, SCREEN_HEIGHT - PIECE_AREA_HEIGHT - 20)
            img = pygame.transform.smoothscale(img, (puzzle_display_size, puzzle_display_size))
            return img, puzzle_display_size
        except pygame.error as e:
            print(f"Error loading image: {e}")
            print(f"Tried path: {image_path}")
            fallback = pygame.Surface((200, 200))
            fallback.fill((255, 0, 0))
            return fallback, 200

    def setup_puzzle(self, pieces_data, rows, cols):
        """初始化拼图区域和碎片"""
        piece_width = self.state['puzzle_size'] // cols
        piece_height = self.state['puzzle_size'] // rows
        offset_x = (SCREEN_WIDTH - self.state['puzzle_size']) // 2
        offset_y = (SCREEN_HEIGHT - PIECE_AREA_HEIGHT - self.state['puzzle_size']) // 2
        
        # 静态bug3: 逻辑上的死代码
        if False:  # 永远不会执行的代码块
            print("这段代码永远不会被执行")
            # 这里可以放置更多复杂的逻辑，但永远不会运行

        self.state['target_areas'] = []
        for data in pieces_data:
            x = offset_x + data['col'] * piece_width
            y = offset_y + data['row'] * piece_height
            area = pygame.Rect(x, y, piece_width, piece_height)
            self.state['target_areas'].append({'rect': area, 'id': data['id']})

        self.state['puzzle_pieces'] = []
        total = len(pieces_data)
        per_row = cols
        num_rows = (total + per_row - 1) // per_row
        area_h = PIECE_AREA_HEIGHT - 20
        area_w = SCREEN_WIDTH - 20
        w = min(piece_width, area_w // per_row)
        h = min(piece_height, area_h // num_rows)
        start_y = SCREEN_HEIGHT - PIECE_AREA_HEIGHT + (PIECE_AREA_HEIGHT - num_rows * h) // 2

        indices = list(range(total))
        random.shuffle(indices)

        for i, idx in enumerate(indices):
            data = pieces_data[idx]
            row = i // per_row
            col = i % per_row
            start_x = 10 + col * w + w // 2 - piece_width // 2
            start_y_pos = start_y + row * h + h // 2 - piece_height // 2
            piece = self.create_piece(data, start_x, start_y_pos)
            self.state['puzzle_pieces'].append(piece)

    def create_piece(self, data, start_x, start_y):
        from game.puzzle_piece import PuzzlePiece
        return PuzzlePiece(data['image'], data['row'], data['col'], data['id'], start_x, start_y)

    def run_game_loop(self):
        """运行游戏主循环"""
        while True:
            dt = self.clock.tick(60)
            current_time = time.time()
            
            # 动态bug2: 可能导致除以零的情况
            # 如果某个条件下start_time比current_time大，会产生负数时间
            if self.state['start_time'] > current_time:
                # 这里不会导致错误，但会产生异常行为
                self.state['time_elapsed'] = -999
            else:
                self.state['time_elapsed'] = int(current_time - self.state['start_time'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_on_exit()
                    return 'quit'

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.save_on_exit()
                    return 'menu'

                self.handle_mouse_event(event)

            self.update_pieces()
            self.draw()

            if all(p.solved for p in self.state['puzzle_pieces']):
                self.on_completion()
                break

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for piece in reversed(self.state['puzzle_pieces']):
                if piece.rect.collidepoint(event.pos):
                    self.state['puzzle_pieces'].remove(piece)
                    self.state['puzzle_pieces'].append(piece)
                    piece.start_drag(event.pos[0], event.pos[1])
                    break

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for piece in self.state['puzzle_pieces']:
                if piece.dragging:
                    piece.stop_drag(self.state['target_areas'], pygame.Rect(0, SCREEN_HEIGHT - PIECE_AREA_HEIGHT, SCREEN_WIDTH, PIECE_AREA_HEIGHT))

        elif event.type == pygame.MOUSEMOTION:
            for piece in self.state['puzzle_pieces']:
                piece.update_position(event.pos[0], event.pos[1])

    def update_pieces(self):
        pass  # 拖拽已在事件中处理

    def draw(self):
        self.ui.draw_game_screen(
            self.screen,
            self.state['puzzle_pieces'],
            self.state['target_areas'],
            self.state['original_image'],
            self.state['time_elapsed'],
            self.state['moves']
        )

    def on_completion(self):
        total_time = self.state['time_elapsed']
        self.ranking_manager.add_record(
            image_id=self.state['selected_image_id'] or "default",
            difficulty=self.state['difficulty'],
            shape=self.state['shape_type'],
            time_taken=total_time,
            moves=self.state['moves']
        )
        self.ui.show_completion_screen(self.screen, total_time)
        self.clear_save_file()  # 完成后删除存档

    def save_on_exit(self):
        state = {
            'image_path': "src/assets/nature/scenery_001.jpg",
            'rows': self.state['difficulty'],
            'cols': self.state['difficulty'],
            'shape_type': self.state['shape_type'],
            'moves': self.state['moves'],
            'start_time': self.state['start_time'],
            'pieces': [{'rect': (p.rect.x, p.rect.y), 'solved': p.solved} for p in self.state['puzzle_pieces']]
        }
        save_game_state(state)

    def clear_save_file(self):
        if os.path.exists("saves/current.json"):
            os.remove("saves/current.json")