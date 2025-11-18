import os
import json
import pygame
from utils.font_loader import load_font
from data.ranking_manager import RankingManager
from data.image_manager import ImageManager
from config import RANKING_DIR, SCREEN_WIDTH, SCREEN_HEIGHT, CUSTOM_IMAGE_DIR

# ===== 按钮类（保留你朋友的视觉交互）=====
class Button:
    def __init__(self, x, y, width, height, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.is_hovered = False
        self.scale_factor = 1.2

    def draw(self, surface):
        if self.image:
            scale = self.scale_factor if self.is_hovered else 1
            sw = int(self.rect.width * scale)
            sh = int(self.rect.height * scale)
            scaled = pygame.transform.smoothscale(self.image, (sw, sh))
            r = scaled.get_rect(center=self.rect.center)
            surface.blit(scaled, r)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def create_horizontal_button_layout(screen_width, screen_height, button_count, button_width, button_height, spacing):
    total_width = button_count * button_width + (button_count - 1) * spacing
    start_x = (screen_width - total_width) // 2
    start_y = screen_height - button_height - 80
    return [(start_x + i * (button_width + spacing), start_y) for i in range(button_count)]


# ===== 小工具 =====
def _safe_index_next(seq, cur):
    if not seq:
        return cur
    try:
        i = seq.index(cur)
        return seq[(i + 1) % len(seq)]
    except ValueError:
        return seq[0]


def _normalize_shape(shape_str: str) -> str:
    if not shape_str:
        return "jigsaw"
    m = {
        "square": "rectangle", "rectangle": "rectangle", "正方形": "rectangle", "方形": "rectangle",
        "triangle": "triangle", "三角形": "triangle",
        "irregular": "jigsaw", "jigsaw": "jigsaw", "不规则": "jigsaw", "凹凸形": "jigsaw"
    }
    return m.get(str(shape_str).lower(), "jigsaw")


# 中文展示名
SHAPE_ZH = {
    "rectangle": "正方形",
    "triangle": "三角形",
    "jigsaw": "凹凸形",
}

def _shape_to_zh(shape_key: str) -> str:
    return SHAPE_ZH.get(_normalize_shape(shape_key), "凹凸形")


def _is_custom_image(image_id: str):
    """是否编辑器自制拼图：src/assets/custom/<image_id>/settings.json 存在"""
    folder = os.path.join(CUSTOM_IMAGE_DIR, image_id)
    settings_path = os.path.join(folder, "settings.json")
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                js = json.load(f)
            order = int(js.get("order", 3))
            shape = _normalize_shape(js.get("shape", "jigsaw"))
            return True, order, shape
        except (ValueError, KeyError, json.JSONDecodeError):
            return True, None, None
    return False, None, None


def _filter_default_from_images(images):
    """如果除了 default 还有其他图片，则去掉 default；否则保留 default 作为占位。"""
    others = [x for x in images if x != "default"]
    return others if others else images


def show_ranking(screen, audio_manager=None):
    font_medium = load_font('zhengwen.ttf', 36)
    font_small  = load_font('zhengwen.ttf', 24)

    rm = RankingManager()
    image_manager = ImageManager()  # 先留着，便于后续扩展

    # 背景
    bg_path = 'src/assets/images/ranking_backgroundImage.png'
    background_image = None
    if os.path.exists(bg_path):
        background_image = pygame.image.load(bg_path).convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # 初始候选集合
    present = rm.get_all_values()
    images = _filter_default_from_images(present.get("images", []) or ["default"])
    diffs  = sorted(present.get("difficulties", [3, 4, 5]) or [3, 4, 5])
    shapes = present.get("shapes", ["jigsaw", "triangle", "rectangle"]) or ["jigsaw", "triangle", "rectangle"]

    # 初始选择
    current_image = images[0]
    current_difficulty = f"{diffs[0]}x{diffs[0]}"
    current_shape = shapes[0]

    # 自制锁定
    difficulty_locked = False
    shape_locked = False

    def apply_lock_for_image(img_id: str):
        nonlocal current_difficulty, current_shape, difficulty_locked, shape_locked
        is_custom, order, shp = _is_custom_image(img_id)
        if is_custom and order and shp:
            current_difficulty = f"{int(order)}x{int(order)}"
            current_shape = _normalize_shape(shp)
            difficulty_locked = True
            shape_locked = True
        else:
            difficulty_locked = False
            shape_locked = False

    apply_lock_for_image(current_image)

    clock = pygame.time.Clock()

    # 资源目录
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.normpath(os.path.join(cur_dir, '..', 'assets'))

    # 按钮（沿用原美术：第5个按钮现在做“删除当前图片记录”）
    button_data = [
        {"image": "switch_image_normal.png"},      # 0 切换图片
        {"image": "switch_difficulty_normal.png"}, # 1 切换难度
        {"image": "switch_shape_normal.png"},      # 2 切换形状
        {"image": "back_normal.png"},              # 3 返回
        {"image": "refresh_normal.png"}            # 4 删除（功能改为删除当前图片的所有记录）
    ]

    BUTTON_WIDTH  = 150
    BUTTON_HEIGHT = 80
    SPACING       = 30

    btn_positions = create_horizontal_button_layout(
        SCREEN_WIDTH, SCREEN_HEIGHT, len(button_data), BUTTON_WIDTH, BUTTON_HEIGHT, SPACING
    )

    buttons = []
    for i, data in enumerate(button_data):
        x, y = btn_positions[i]
        image_path = os.path.join("src", "assets", 'images', 'buttons', data["image"])
        print(f"Loading button image: {image_path}")
        if not os.path.exists(image_path):
            print(f"⚠️ 文件不存在: {image_path}")
            button_img = None
        else:
            button_img = pygame.image.load(image_path)
        buttons.append(Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, button_img))

    TOP_N = 5  # 仅显示前5条

    # 删除当前图片的所有记录，并前进到下一张
    def delete_current_image_records():
        nonlocal images, current_image, current_difficulty, current_shape
        # 使用 RankingManager 的内部数据进行删除并保存
        try:
            rm._data = [r for r in rm._data if r.get("image") != current_image]  # 直接操作内部列表
            rm._save()
        except Exception as e:
            print(f"删除失败: {e}")

        # 刷新候选
        present2 = rm.get_all_values()
        new_images = _filter_default_from_images(present2.get("images", []) or ["default"])

        # 如果当前图片已不在列表，顺延到下一张
        if current_image not in new_images:
            images = new_images or ["default"]
            current_image = images[0]
            # 重新根据图片决定锁定
            apply_lock_for_image(current_image)
        else:
            images = new_images

        # 同步难度/形状候选（一般不需要，但保险起见）
        diffs2  = sorted(present2.get("difficulties", diffs) or diffs)
        shapes2 = present2.get("shapes", shapes) or shapes
        # 如果锁定则不变，否则保持现有或回退到候选首位
        if not difficulty_locked:
            try:
                cur_num = int(current_difficulty.split('x')[0])
                if cur_num not in diffs2:
                    current_difficulty = f"{diffs2[0]}x{diffs2[0]}"
            except Exception:
                current_difficulty = f"{diffs2[0]}x{diffs2[0]}"
        if not shape_locked:
            if current_shape not in shapes2:
                current_shape = shapes2[0]

    while True:
        # 背景
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((255, 255, 255))

        # 列布局
        COL_START = SCREEN_WIDTH // 8 + 50
        COL_RANK  = COL_START
        COL_TIME  = COL_START + 100
        COL_DATE  = COL_START + 230

        # 标题
        title = font_medium.render("🏆 排行榜 - 最佳时间", True, (0, 0, 0))
        screen.blit(title, (COL_START + (SCREEN_WIDTH // 4 - title.get_width() // 2) - 50, 180))

        # 锁定提示
        lock_suffix = []
        if difficulty_locked:
            lock_suffix.append("自制图片")
        if shape_locked:
            lock_suffix.append("已锁定")
        lock_text = f"（{'，'.join(lock_suffix)}）" if lock_suffix else ""

        # 形状使用中文显示
        selection_text = font_small.render(
            f"图片: {current_image} | 难度: {current_difficulty} | 形状: {_shape_to_zh(current_shape)} {lock_text}",
            True, (0, 0, 0)
        )
        screen.blit(selection_text, (COL_START + (SCREEN_WIDTH // 4 - selection_text.get_width() // 2) - 50, 230))

        # 解析难度
        try:
            difficulty_num = int(current_difficulty.split('x')[0])
        except Exception:
            difficulty_num = diffs[0]
            current_difficulty = f"{difficulty_num}x{difficulty_num}"

        # 当前筛选记录
        records = rm.get_records(
            image=current_image,
            difficulty=difficulty_num,
            shape=_normalize_shape(current_shape),
            limit=1_000_000
        )
        best_count = len(records)

        # 该图片的“游玩次数”（所有难度与形状）
        plays_for_image = rm.get_records(image=current_image, difficulty=None, shape=None, limit=1_000_000)
        play_count = len(plays_for_image)

        if best_count == 0:
            # 统计条
            count_text = font_small.render(
                f"本图游玩次数：{play_count}   选定类型共 {best_count} 条最佳纪录",
                True, (0, 100, 0)
            )
            screen.blit(count_text, (COL_START + (SCREEN_WIDTH // 4 - count_text.get_width() // 2) - 50, 280))

            no_data = font_medium.render("暂无成绩记录", True, (100, 100, 100))
            screen.blit(no_data, (COL_START + (SCREEN_WIDTH // 4 - no_data.get_width() // 2) - 50, 320))

            hint_text = font_small.render("请先完成一局游戏来生成记录", True, (200, 0, 0))
            screen.blit(hint_text, (COL_START + (SCREEN_WIDTH // 4 - hint_text.get_width() // 2) - 50, 360))
        else:
            count_text = font_small.render(
                f"本图游玩次数：{play_count}   选定类型共 {best_count} 条最佳纪录（显示前 {min(TOP_N, best_count)} 条）",
                True, (0, 100, 0)
            )
            screen.blit(count_text, (COL_START + (SCREEN_WIDTH // 4 - count_text.get_width() // 2) - 50, 280))

            # 表头
            header_rank = font_small.render("排名", True, (0, 0, 100))
            header_time = font_small.render("时间(秒)", True, (0, 0, 100))
            header_date = font_small.render("日期", True, (0, 0, 100))

            screen.blit(header_rank, (COL_RANK, 330))
            screen.blit(header_time, (COL_TIME, 330))
            screen.blit(header_date, (COL_DATE, 330))

            line_left = COL_RANK
            line_right = COL_DATE + header_date.get_width()
            pygame.draw.line(screen, (200, 200, 200), (line_left, 355), (line_right, 355), 2)

            # 前 TOP_N
            for i, record in enumerate(records[:TOP_N]):
                rank_text = f"{i+1:2d}"
                time_text = f"{record.get('elapsed', 0):6d}s"
                date_text = record.get('finished_at', '')

                y_pos = 360 + i * 35
                screen.blit(font_small.render(rank_text, True, (0, 0, 0)), (COL_RANK, y_pos))
                screen.blit(font_small.render(time_text, True, (0, 100, 0)), (COL_TIME, y_pos))
                screen.blit(font_small.render(str(date_text), True, (0, 0, 100)), (COL_DATE, y_pos))

        # 按钮悬停 & 绘制
        mouse_pos = pygame.mouse.get_pos()
        for b in buttons:
            b.check_hover(mouse_pos)
            b.draw(screen)

        # 事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 0: 切换图片（跳过 default，如果还有其他图片）
                if buttons[0].is_clicked(event):
                    # 重新过滤一次，避免删除后又出现 default 的情况
                    images = _filter_default_from_images(images)
                    current_image = _safe_index_next(images, current_image)
                    apply_lock_for_image(current_image)
                    print(f"切换到图片: {current_image}（锁定: diff={difficulty_locked}, shape={shape_locked}）")

                # 1: 切换难度
                elif buttons[1].is_clicked(event):
                    if not difficulty_locked:
                        next_diff = _safe_index_next(diffs, int(current_difficulty.split('x')[0]))
                        current_difficulty = f"{next_diff}x{next_diff}"
                        print(f"切换到难度: {current_difficulty}")
                    else:
                        print("难度被锁定，无法切换。")

                # 2: 切换形状（中文展示，内部英文键）
                elif buttons[2].is_clicked(event):
                    if not shape_locked:
                        current_shape = _safe_index_next(shapes, _normalize_shape(current_shape))
                        print(f"切换到形状: {_shape_to_zh(current_shape)}")
                    else:
                        print("形状被锁定，无法切换。")

                # 3: 返回
                elif buttons[3].is_clicked(event):
                    return 'menu'

                # 4: 删除当前图片的全部记录（功能替代原“刷新”）
                elif buttons[4].is_clicked(event):
                    print(f"删除图片 '{current_image}' 的所有排行榜记录...")
                    delete_current_image_records()

        pygame.display.flip()
        clock.tick(60)