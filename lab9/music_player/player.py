import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        # 自动加载 music 文件夹里的音乐
        self.playlist = [f"music/{f}" for f in os.listdir("music") 
                        if f.endswith((".mp3", ".wav"))]
        self.current = 0
        self.playing = False

    # 播放当前歌曲
    def play(self):
        if not self.playlist:
            return
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()
        self.playing = True

    # 停止
    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    # 下一首
    def next(self):
        if not self.playlist:
            return
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    # 上一首
    def back(self):
        if not self.playlist:
            return
        self.current = (self.current - 1) % len(self.playlist)
        self.play()

    # 获取当前歌曲名
    def get_song(self):
        if not self.playlist:
            return "No music"
        return os.path.basename(self.playlist[self.current])