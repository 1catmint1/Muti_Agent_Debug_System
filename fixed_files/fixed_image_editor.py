# ui/image_editor_ui.py
import pygame
from tkinter import Tk, filedialog
from PIL import Image
import os
from config import CUSTOM_IMAGE_DIR

def prompt_file():
    """打开文件选择对话框"""
    top = Tk()
    top.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_path

def show_image_editor(screen):
    # 假设font已经加载，这里简化处理
    font = pygame.font.SysFont(None, 36)
    manager = None  # 假设ImageManager的初始化逻辑需要根据实际代码调整

    clock = pygame.time.Clock()
    while True:
        screen.fill((220, 220, 220))
        title = font.render("🖼️ 自定义图片", True, (0, 0, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))

        instructions = font.render("点击下方按钮选择图片", True, (100, 100, 100))
        screen.blit(instructions, (screen.get_width()//2 - instructions.get_width()//2, 150))

        select_btn = pygame.Rect(350, 250, 200, 50)
        pygame.draw.rect(screen, (180, 180, 180), select_btn)
        select_text = font.render("选择图片", True, (0, 0, 0))
        screen.blit(select_text, select_text.get_rect(center=select_btn.center))

        back_btn = pygame.Rect(350, 500, 200, 50)
        pygame.draw.rect(screen, (180, 180, 180), back_btn)
        back_text = font.render("返回", True, (0, 0, 0))
        screen.blit(back_text, back_text.get_rect(center=back_btn.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_btn.collidepoint(event.pos):
                    # 打开文件选择器
                    file_path = prompt_file()
                    if file_path and os.path.exists(file_path):
                        # 复制文件到自定义目录
                        dest = os.path.join(CUSTOM_IMAGE_DIR, os.path.basename(file_path))
                        try:
                            with open(dest, 'wb') as f_dest, open(file_path, 'rb') as f_src:
                                f_dest.write(f_src.read())
                            # 更新ImageManager中的数据
                            # manager.load_custom_images()
                            # 显示缩略图
                            image = Image.open(dest)
                            image.thumbnail((100, 100))
                            thumb_path = os.path.splitext(dest)[0] + "_thumb.png"
                            image.save(thumb_path)
                            print(f"成功导入图片: {os.path.basename(file_path)}")
                        except Exception as e:
                            print(f"无法处理图片: {e}")
                elif back_btn.collidepoint(event.pos):
                    return 'menu'

        pygame.display.flip()
        clock.tick(60)