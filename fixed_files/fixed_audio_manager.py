# utils/audio_manager.py
import pygame
import os

class AudioManager:
    def __init__(self):
        self.music_volume = 0.3   # 0.0 ~ 1.0
        self.sfx_volume = 0.5     # 音效音量
        self.bgm_loaded = False

    def load_background_music(self, music_path):
        """加载背景音乐（不自动播放）"""
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                self.bgm_loaded = True
                print(f"【音频】加载背景音乐: {music_path}")
            except pygame.error as e:
                print(f"【音频错误】加载背景音乐失败: {e}")
        else:
            print(f"【音频警告】背景音乐文件不存在: {music_path}")

    def play_background_music(self, loops=-1):
        """播放背景音乐"""
        if self.bgm_loaded:
            pygame.mixer.music.play(loops=loops)
            print("【音频】开始播放背景音乐")

    def set_music_volume(self, volume):
        """设置背景音乐音量（0.0 ~ 1.0）"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        print(f"【音频】背景音乐音量设置为: {self.music_volume:.2f}")

    def play_correct_sound(self, sfx_path):
        """播放“正确”音效"""
        if os.path.exists(sfx_path):
            try:
                sound = pygame.mixer.Sound(sfx_path)
                sound.set_volume(self.sfx_volume)
                sound.play()
            except pygame.error as e:
                print(f"【音频错误】播放音效失败: {e}")
        else:
            print(f"【音频警告】音效文件不存在: {sfx_path}")