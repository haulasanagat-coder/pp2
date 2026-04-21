import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        # Load playlist automatically
        self.playlist = [f"music/{f}" for f in os.listdir("music") 
                        if f.endswith((".mp3", ".wav"))]
        self.current = 0
        self.playing = False

    # Play function
    def play(self):
        if not self.playlist:
            return
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()
        self.playing = True

    # Stop function
    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    # Next song
    def next(self):
        if not self.playlist:
            return
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    # Previous song
    def back(self):
        if not self.playlist:
            return
        self.current = (self.current - 1) % len(self.playlist)
        self.play()

    # Get current song name
    def get_song(self):
        if not self.playlist:
            return "No music"
        return os.path.basename(self.playlist[self.current])