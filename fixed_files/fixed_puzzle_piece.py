import pygame

class PuzzlePiece:
    def __init__(self, image, row, col, piece_id, start_x, start_y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.start_pos = (start_x, start_y)
        self.row = row
        self.col = col
        self.id = piece_id
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.solved = False
        self.mask = pygame.mask.from_surface(self.image)

        # 创建一个半透明背景 Surface (这部分逻辑可以简化或移除)
        self.bg_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.bg_surface.fill((240, 240, 240, 150))
        pygame.draw.rect(self.bg_surface, (100, 100, 100, 200), (0, 0, self.rect.width, self.rect.height), 1)

    def start_drag(self, mouse_x, mouse_y):
        if not self.solved:
            self.dragging = True
            self.offset_x = self.rect.x - mouse_x
            self.offset_y = self.rect.y - mouse_y

    def stop_drag(self, target_areas, piece_area_rect):
        if self.dragging:
            self.dragging = False
            center_x, center_y = self.rect.center

            for area in target_areas:
                if area.rect.collidepoint(center_x, center_y):  # 中心点落在该区域
                    print(str(self.id),end=str(area.piece_ids))
                    if self.id in area.piece_ids:  # ✅ 检查 id 是否被接受
                        self.rect.center = area.rect.center
                        self.solved = True
                        return True
                    else:
                        # 放错位置（比如 id=0 放到只有 [2,3] 的区域）
                        self.rect.topleft = self.start_pos
                        return False

            # 没有放入任何目标区域
            # self.rect.topleft = self.start_pos
            return False
        return False

    def update_position(self, mouse_x, mouse_y):
        if self.dragging:
            self.rect.x = mouse_x + self.offset_x
            self.rect.y = mouse_y + self.offset_y

    def draw(self, surface, in_piece_area=False):
        # --- 原始绘制 ---
        surface.blit(self.image, self.rect)

        # # --- 【新增】绘制红色碰撞框 ---
        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)  # 红色边框表示 rect 区域s

        # # --- 【新增】绘制编号 ---
        # from config import FONT_SIZES
        # from game.game_logic import load_font
        # font = load_font(max(12, FONT_SIZES['small'] // 2))
        # text_surface = font.render(str(self.id), True, (255, 255, 255))  # 白字
        # text_rect = text_surface.get_rect(center=self.rect.center)
        # surface.blit(text_surface, text_rect)