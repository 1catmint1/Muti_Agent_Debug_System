# utils/font_loader.py
import pygame
import os

def load_font(font_name, size):
    font_path = os.path.join('src', 'assets', 'fonts', font_name)
    try:
        return pygame.font.Font(font_path, size)
    except FileNotFoundError:
        print(f"Font file not found: {font_path}")
        return pygame.font.SysFont(None, size)  # 使用系统默认字体作为回退选项