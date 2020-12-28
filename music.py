from game_settings import *
import pygame


class Music:
    def __init__(self):
        pygame.mixer.music.load(LEVEL_MUSIC)

    def play(self, volume=1.0):
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
