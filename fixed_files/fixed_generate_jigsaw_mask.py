# game/generate_jigsaw_mask.py
"""
使用 PIL 生成锯齿状拼图遮罩并切割图像，修改为可返回 Pygame Surface。
"""

from PIL import Image, ImageDraw, ImageOps
import os
import pygame # 新增导入

class PuzzlePiece:
    """代表单个拼图块"""
    def __init__(self, image, row, col, num_pieces, bbox=None):
        self.image = image
        self.original_image = image.copy()
        # 存储在原始图像中的边界框 (left, upper, right, lower)
        self.bbox = bbox if bbox else (0, 0, image.width, image.height)
        self.row = row
        self.col = col
        self.num_pieces = num_pieces
        self.rotation = 0  # 0, 90, 180, 270
        self.flipped = False

    def rotate(self):
        """顺时针旋转90度"""
        self.rotation = (self.rotation + 90) % 360
        self.image = self.original_image.rotate(self.rotation, expand=True)
        if self.flipped:
            self.image = ImageOps.mirror(self.image)

    def flip(self):
        """水平翻转"""
        self.flipped = not self.flipped
        self.image = self.original_image.rotate(self.rotation, expand=True)
        if self.flipped:
            self.image = ImageOps.mirror(self.image)

    def reset(self):
        """重置变换"""
        self.rotation = 0
        self.flipped = False
        self.image = self.original_image.copy()

    def _create_square_puzzle_pieces(self, num_pieces):
        """创建方形拼图块"""
        if not self.image:
            return

        width, height = self.image.size
        piece_width = width // num_pieces
        piece_height = height // num_pieces

        self.pieces = []
        for i in range(num_pieces):
            for j in range(num_pieces):
                left = j * piece_width
                top = i * piece_height
                right = min((j + 1) * piece_width, width)  # 确保不超出边界
                bottom = min((i + 1) * piece_height, height)

                piece = self.image.crop((left, top, right, bottom))
                # 对于方形，bbox 是基于规则网格的
                puzzle_piece = PuzzlePiece(piece, i, j, num_pieces, bbox=(left, top, right, bottom))
                self.pieces.append(puzzle_piece)

    def _create_triangle_puzzle_pieces(self, num_pieces):
        """创建三角形拼图块 (简化版)"""
        if not self.image:
            return

        width, height = self.image.size
        self.pieces = []

        # 分割成方形，然后切成三角形
        square_size = min(width, height) // num_pieces
        rows = height // square_size
        cols = width // square_size

        piece_index = 0
        for i in range(rows):
            for j in range(cols):
                left = j * square_size
                top = i * square_size
                right = min(left + square_size, width)
                bottom = min(top + square_size, height)

                square_piece = self.image.crop((left, top, right, bottom))
                square_width, square_height = square_piece.size

                # 创建两个三角形 (左上和右下)
                # 左上三角形
                mask = Image.new('L', (square_width, square_height), 0)
                draw = ImageDraw.Draw(mask)
                draw.polygon([(0, 0), (square_width, 0), (0, square_height)], fill=255)
                triangle1 = Image.new('RGBA', (square_width, square_height))
                triangle1.paste(square_piece, (0, 0), mask)
                bbox1 = mask.getbbox()
                if bbox1:
                    # 调整bbox到原始图像坐标
                    abs_bbox1 = (left + bbox1[0], top + bbox1[1], left + bbox1[2], top + bbox1[3])
                    triangle1 = triangle1.crop(bbox1)
                    puzzle_piece1 = PuzzlePiece(triangle1, i, j, num_pieces, bbox=abs_bbox1)
                    self.pieces.append(puzzle_piece1)

                # 右下三角形
                mask = Image.new('L', (square_width, square_height), 0)
                draw = ImageDraw.Draw(mask)
                draw.polygon([(square_width, square_height), (square_width, 0), (0, square_height)], fill=255)
                triangle2 = Image.new('RGBA', (square_width, square_height))
                triangle2.paste(square_piece, (0, 0), mask)
                bbox2 = mask.getbbox()
                if bbox2:
                    # 调整bbox到原始图像坐标
                    abs_bbox2 = (left + bbox2[0], top + bbox2[1], left + bbox2[2], top + bbox2[3])
                    triangle2 = triangle2.crop(bbox2)
                    puzzle_piece2 = PuzzlePiece(triangle2, i, j, num_pieces, bbox=abs_bbox2)
                    self.pieces.append(puzzle_piece2)

                piece_index += 2


def gen_jigsaw_mask(size, tab_size, top, bottom, left, right):
    """生成单个拼图块的遮罩"""
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    w, h = size
    # 主体矩形
    draw.rectangle([tab_size, tab_size, w-tab_size, h-tab_size], fill=255)
    # 上边
    if top == "tab":
        draw.ellipse([w//2-tab_size//2, tab_size//2, w//2+tab_size//2, tab_size+tab_size//2], fill=255)
    elif top == "slot":
        draw.ellipse([w//2-tab_size//2, tab_size//2, w//2+tab_size//2, tab_size + tab_size//2], fill=0)
    # 下边
    if bottom == "tab":
        draw.ellipse([w//2-tab_size//2, h-tab_size-tab_size//2, w//2+tab_size//2, h-tab_size//2], fill=255)
    elif bottom == "slot":
        draw.ellipse([w//2-tab_size//2, h-tab_size-tab_size//2, w//2+tab_size//2, h-tab_size//2], fill=0)
    # 左边
    if left == "tab":
        draw.ellipse([tab_size//2, h//2-tab_size//2, tab_size+tab_size//2, h//2+tab_size//2], fill=255)
    elif left == "slot":
        draw.ellipse([tab_size//2, h//2-tab_size//2, tab_size+tab_size//2, h//2+tab_size//2], fill=0)
    # 右边
    if right == "tab":
        draw.ellipse([w-tab_size-tab_size//2, h//2-tab_size//2, w-tab_size//2, h//2+tab_size//2], fill=255)
    elif right == "slot":
        draw.ellipse([w-tab_size-tab_size//2, h//2-tab_size//2, w-tab_size//2, h//2+tab_size//2], fill=0)
    return mask

def get_edge_type(row, col, rows, cols, edge):
    """根据行列和边缘确定是 'tab', 'slot' 还是 'flat'"""
    # 四边界为flat，其余按行列偶奇决定凹凸
    if edge == "top":
        return "flat" if row == 0 else ("tab" if col % 2 == 0 else "slot")
    if edge == "bottom":
        return "flat" if row == rows-1 else ("tab" if col % 2 == 1 else "slot")
    if edge == "left":
        return "flat" if col == 0 else ("tab" if row % 2 == 0 else "slot")
    if edge == "right":
        return "flat" if col == cols-1 else ("tab" if row % 2 == 1 else "slot")
    return "flat"

def split_image_with_jigsaw_mask(img_path, rows, cols, out_dir="output_pieces", return_surfaces=False):
    """
    切割图像并生成锯齿状拼图块。
    :param img_path: 原始图像路径
    :param rows: 行数
    :param cols: 列数
    :param out_dir: 输出目录 (仅在 return_surfaces=False 时使用)
    :param return_surfaces: 是否返回 Pygame Surface 列表而不是保存文件
    :return: 如果 return_surfaces 为 True，则返回包含 {'image', 'row', 'col', 'id'} 字典的列表；否则返回 None。
    """
    try:
        img = Image.open(img_path).convert("RGBA")
    except Exception as e:
        print(f"打开图片失败 {img_path}: {e}")
        # 如果无法打开图片，直接返回
        if return_surfaces:
            return [] # 返回空列表，表示没有生成任何碎片
        else:
            return # 直接返回 None
        
    w, h = img.size
    piece_w, piece_h = w // cols, h // rows
    tab_size = min(piece_w, piece_h) // 4  # 凸起/凹陷高度

    if not return_surfaces:
        os.makedirs(out_dir, exist_ok=True)
        
    surfaces = [] if return_surfaces else None

    for row in range(rows):
        for col in range(cols):
            # 遮照区域（留凸起空间）
            mask_size = (piece_w + tab_size * 2, piece_h + tab_size * 2)
            # 生成遮照
            top = get_edge_type(row, col, rows, cols, "top")
            bottom = get_edge_type(row, col, rows, cols, "bottom")
            left = get_edge_type(row, col, rows, cols, "left")
            right = get_edge_type(row, col, rows, cols, "right")
            mask = gen_jigsaw_mask(mask_size, tab_size, top, bottom, left, right)
            
            # 裁剪原图对应区域
            crop_left = col * piece_w - tab_size
            crop_top = row * piece_h - tab_size
            crop_box = (
                max(crop_left, 0),
                max(crop_top, 0),
                min(crop_left + mask_size[0], w),
                min(crop_top + mask_size[1], h)
            )
            piece_img = Image.new("RGBA", mask_size, (0,0,0,0))
            try:
                crop_img = img.crop(crop_box)
                paste_x = max(0, -crop_left)
                paste_y = max(0, -crop_top)
                piece_img.paste(crop_img, (paste_x, paste_y))
            except Exception as e:
                print(f"裁剪图片时出错 (row={row}, col={col}): {e}")
                # 可以选择跳过这个碎片或创建一个空白的
                # 这里我们继续，让遮罩决定最终外观
                
            # 遮照应用
            piece_img.putalpha(mask)
            
            if return_surfaces:
                try:
                    # 转换为 Pygame Surface
                    mode = piece_img.mode
                    size = piece_img.size
                    data = piece_img.tobytes()
                    pygame_surface = pygame.image.fromstring(data, size, mode)
                    surfaces.append({
                        'image': pygame_surface,
                        'row': row,
                        'col': col,
                        'id': row * cols + col
                    })
                except Exception as e:
                    print(f"转换为 Pygame Surface 时出错 (row={row}, col={col}): {e}")
                    # 可以选择跳过或添加一个默认的 Surface
            else:
                fname = f"piece_{row}_{col}.png"
                try:
                    piece_img.save(os.path.join(out_dir, fname))
                    print(f"Saved {fname}")
                except Exception as e:
                    print(f"保存图片失败 {fname}: {e}")

    if return_surfaces:
        return surfaces
    # 如果 return_surfaces 为 False，函数执行到这里自然结束，等同于 return None
    # 显式写出 return 也是可以的，但不是必须的
    return # 或者省略这行

def draw_jigsaw_outline_on_image(image, rows, cols, outline_color=(255, 0, 0, 255), output_path=None):
    """
    在原图上绘制拼图切割轮廓线，直观展示拼图块的锯齿边界。
    :param img_path: 原始图像路径
    :param rows: 拼图行数
    :param cols: 拼图列数
    :param outline_color: 轮廓线颜色 (R, G, B, A)，RGBA
    :param output_path: 输出图像路径，若为 None 则不保存
    :return: 带轮廓线的 PIL Image 对象
    """
    try:
        # 确保图像是 RGBA 模式以便处理透明度
        img = image.convert("RGBA")
    except Exception as e:
        print(f"处理输入的 PIL 图像失败: {e}")
        return None

    w, h = img.size
    piece_w, piece_h = w // cols, h // rows
    tab_size = min(piece_w, piece_h) // 6  # 凸起/凹陷大小

    # 创建一个透明图层用于绘制轮廓
    outline_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(outline_layer)

    def draw_bump_line(x0, y0, x1, y1, direction, is_tab):
        """绘制带凸起或凹陷的线段（水平或垂直）"""
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        r = tab_size

        if direction == "horizontal":
            if is_tab:
                # 凸起：向上半圆
                draw.arc([cx - r, y0 - r, cx + r, y0 + r], start=0, end=180, fill=outline_color)
                draw.line([x0, y0, cx - r, y0], fill=outline_color)
                draw.line([cx + r, y0, x1, y0], fill=outline_color)
            else:
                # 凹陷：向下挖半圆
                draw.arc([cx - r, y1 - r, cx + r, y1 + r], start=180, end=360, fill=outline_color)
                draw.line([x0, y1, cx - r, y1], fill=outline_color)
                draw.line([cx + r, y1, x1, y1], fill=outline_color)
        elif direction == "vertical":
            if is_tab:
                # 凸起：向右半圆
                draw.arc([x1 - r, cy - r, x1 + r, cy + r], start=90, end=270, fill=outline_color)
                draw.line([x1, y0, x1, cy - r], fill=outline_color)
                draw.line([x1, cy + r, x1, y1], fill=outline_color)
            else:
                # 凹陷：向左挖半圆
                draw.arc([x0 - r, cy - r, x0 + r, cy + r], start=-90, end=90, fill=outline_color)
                draw.line([x0, y0, x0, cy - r], fill=outline_color)
                draw.line([x0, cy + r, x0, y1], fill=outline_color)

    for row in range(rows):
        for col in range(cols):
            x = col * piece_w
            y = row * piece_h
            right = x + piece_w
            bottom = y + piece_h

            # 获取四边类型
            top_type = get_edge_type(row, col, rows, cols, "top")
            bottom_type = get_edge_type(row, col, rows, cols, "bottom")
            left_type = get_edge_type(row, col, rows, cols, "left")
            right_type = get_edge_type(row, col, rows, cols, "right")

            # # 上边（水平线，y = y）
            # if row == 0 or top_type != "flat":
            #     if top_type == "tab":
            #         draw_bump_line(x, y, right, y, "horizontal", True)
            #     elif top_type == "slot":
            #         draw_bump_line(x, y, right, y, "horizontal", False)
            #     else:
            #         draw.line([x, y, right, y], fill=outline_color)

            # 下边（水平线，y = bottom）
            if row == rows - 1 or bottom_type != "flat":
                if bottom_type == "tab":
                    draw_bump_line(x, bottom, right, bottom, "horizontal", True)
                elif bottom_type == "slot":
                    draw_bump_line(x, bottom, right, bottom, "horizontal", False)
                else:
                    draw.line([x, bottom, right, bottom], fill=outline_color)

            # 左边（垂直线，x = x）
            if col == 0 or left_type != "flat":
                if left_type == "tab":
                    draw_bump_line(x, y, x, bottom, "vertical", True)
                elif left_type == "slot":
                    draw_bump_line(x, y, x, bottom, "vertical", False)
                else:
                    draw.line([x, y, x, bottom], fill=outline_color)

            # # 右边（垂直线，x = right）
            # if col == cols - 1 or right_type != "flat":
            #     if right_type == "tab":
            #         draw_bump_line(right, y, right, bottom, "vertical", True)
            #     elif right_type == "slot":
            #         draw_bump_line(right, y, right, bottom, "vertical", False)
            #     else:
            #         draw.line([right, y, right, bottom], fill=outline_color)

    # 合并原图与轮廓图层
    result = Image.alpha_composite(img, outline_layer)

    if output_path:
        result.save(output_path)
        print(f"轮廓图已保存至: {output_path}")

    return result




