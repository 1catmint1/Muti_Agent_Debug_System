# game/puzzle_rotation.py

import pygame


def rotate_piece(piece, angle):
    """
    旋转指定的拼图块。
    
    :param piece: PuzzlePiece 实例
    :param angle: 旋转角度（通常为 90 的倍数，正数表示逆时针，负数表示顺时针）
    """
    # 原始图像只保留一次（避免重复旋转失真）
    if not hasattr(piece, 'original_image'):
        piece.original_image = piece.image.copy()

    # 累积旋转角度
    piece.rotation_angle = getattr(piece, 'rotation_angle', 0)
    new_angle = (piece.rotation_angle + angle) % 360
    piece.rotation_angle = new_angle

    # 重新旋转原始图像
    piece.image = pygame.transform.rotate(piece.original_image, -new_angle)  # Pygame 旋转是顺时针为正

    # 更新 rect 以保持中心不变
    old_center = piece.rect.center
    piece.rect = piece.image.get_rect(center=old_center)


def reset_rotation(piece):
    if hasattr(piece, 'original_image'):
        piece.image = piece.original_image.copy()
        piece.rect = piece.image.get_rect(center=piece.rect.center)
    piece.rotation_angle = 0


def handle_rotation_input(event, selected_piece):
    if not selected_piece:
        return False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            selected_piece.rotate(90)
            return True
        elif event.key == pygame.K_RIGHT:
            selected_piece.rotate(-90)
            return True

    return False