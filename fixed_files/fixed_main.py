# main.py
import sys
import pygame
import os
import time

# --- 添加项目根目录到 sys.path ---
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# --- 导入配置 ---
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# --- 导入UI模块 ---
from ui.main_menu_ui import show_main_menu

# --- 导入游戏逻辑模块 ---
from game.game_logic import GameController

# --- 主函数 ---
def main():
    pygame.init()
    
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    except TypeError:
        screen = pygame.display.set_mode((800, 600))
    
    pygame.display.set_caption("智慧拼图")
    clock = pygame.time.Clock()
    
    while True:
        print("【DEBUG】进入主菜单...")
        action = show_main_menu(screen)
        print(f"【DEBUG】用户选择: {action}")

        if action == 'quit':
            print("退出游戏")
            break

        elif action == 'start':
            print("开始新游戏")
            controller = GameController(screen)
            result = controller.start_new_game()
            if result == 'quit':
                break

        elif action == 'load':
            print("加载存档")
            controller = GameController(screen)
            result = controller.load_game()
            if result == 'quit':
                break

        elif action == 'settings':
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"【提示】系统设置暂未实现, 当前时间: {current_time}")

        elif action == 'ranking':
            print("进入排行榜")
            print("【提示】排行榜暂未实现")

        elif action == 'editor':
            print("进入拼图编辑器")
            print("【提示】拼图编辑器暂未实现")

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()