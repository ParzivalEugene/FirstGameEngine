from level import *
from game_settings import *
from ray_cast import ray_casting
import pygame
from collections import deque


class Streaming:
    def __init__(self, screen, map_mini, player):
        self.screen = screen
        self.mini_map = map_mini
        self.player = player
        self.font = pygame.font.SysFont('Arial', 32)
        self.textures = {1: pygame.image.load('textures/wall/STARTAN2.png').convert(),
                         2: pygame.image.load('textures/wall/CEMENT4.png').convert(),
                         3: pygame.image.load('textures/wall/CEMENT3.png').convert(),
                         4: pygame.image.load('textures/wall/STARTAN3.png').convert(),
                         5: pygame.image.load('textures/wall/CEMPOIS.png').convert(),
                         6: pygame.image.load('textures/wall/MARBFAC2.png').convert(),
                         7: pygame.image.load('textures/wall/STARG2.png').convert(),
                         8: pygame.image.load('textures/wall/STARG3.png').convert(),
                         9: pygame.image.load('textures/wall/TEKWALL4.png').convert(),
                         'sky': pygame.image.load('textures/background/night_sky.png'). convert()}
        self.weapon_start_sprite = pygame.image.load('textures/weapons/shotgun/'
                                                     '0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'textures/weapons/shotgun/'
                                                              f'{i}.png').convert_alpha()
                                            for i in range(20)])
        self.weapon_rect = self.weapon_start_sprite.get_rect()
        self.weapon_pos = (HALF_WIDTH - self.weapon_rect.width // 2,
                           HEIGHT - self.weapon_rect.height)
        self.shot_range = len(self.weapon_shot_animation)
        self.shot_sound = pygame.mixer.Sound('sounds/shotgun.wav')
        self.shot_range_count = 0
        self.shot_animation_speed = 4
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.sfx = deque([pygame.image.load(f'textures/weapons/sfx/{i}.png').convert_alpha() for i
                          in range(9)])
        self.sfx_count = 0
        self.sfx_length = len(self.sfx)

    def player_weapon(self, shots):
        if self.player.shot:
            if not self.shot_range_count:
                self.shot_sound.set_volume(0.2)
                self.shot_sound.play()
            self.shot_projection = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.screen.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_range_count += 1
                self.shot_animation_trigger = False
            if self.shot_range_count == self.shot_range:
                self.player.shot = False
                self.shot_range_count = 0
                self.sfx_count = 0
                self.shot_animation_trigger = True
        else:
            self.screen.blit(self.weapon_start_sprite, self.weapon_pos)

    def bullet_sfx(self):
        if self.sfx_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.screen.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
            self.sfx_count += 1
            self.sfx.rotate(-1)

    def check_fps(self, time):  # проверка фпс для отладки
        fps = str(int(time.get_fps()))
        show = self.font.render(fps, 0, GREEN)
        self.screen.blit(show, (WIDTH - 60, 0))

    def draw_background(self, angle):
        # sky_offset = -10 * degrees(angle) % WIDTH
        # self.screen.blit(self.textures['sky'], (sky_offset, 0))
        # self.screen.blit(self.textures['sky'], (sky_offset + WIDTH, 0))
        # self.screen.blit(self.textures['sky'], (sky_offset - WIDTH, 0))
        # pygame.draw.rect(self.screen, GROUND_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.screen, BLACK, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.screen, GROUND_COLOR, (0, 0, WIDTH, HALF_HEIGHT))

    def draw_environment(self, level_objects):
        for obj in sorted(level_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                checker, object_, object_position = obj
                self.screen.blit(object_, object_position)

    def draw_mini_map(self, player):
        self.mini_map.fill(BLACK)
        x, y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.mini_map, WHITE, (x, y),
                         (x + 12 * cos(player.angle),
                          y + 12 * sin(player.angle)))
        pygame.draw.circle(self.mini_map, GREEN, (x, y), 5)

        for x, y in mini_map:
            pass
            pygame.draw.rect(self.mini_map, MINI_MAP_COLOR, (x, y, MAP_CELL, MAP_CELL))
        self.screen.blit(self.mini_map, MAP_POSITION)
