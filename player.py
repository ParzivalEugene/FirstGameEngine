# Файл описывающий игрока
import pygame
from game_settings import *
from level import walls_collision


class Player:
    def __init__(self, sprites):
        self.x, self.y = PLAYER_POSITION
        self.sprites = sprites
        self.angle = PLAYER_ANGLE
        self.sensitivity = 0.002
        self.side = 50
        self.rect = pygame.Rect(*PLAYER_POSITION, self.side, self.side)
        self.shot = False

    @property
    def collisions(self):
        return walls_collision + [pygame.Rect(*i.pos(), i.side, i.side) for i in self.sprites.sprites
                                  if i.blocked]

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collisions)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collisions[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top
            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def collision(self):
        return walls_collision + self.sprites_collision + [pygame.Rect(*i.pos(), i.side, i.side) for
                                                           i in self.sprites.sprites if i.blocked]

    def move(self):
        self.keys()
        self.mouse()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys(self):
        buttons = pygame.key.get_pressed()
        sin_angle, cos_angle = sin(self.angle), cos(self.angle)

        if buttons[pygame.K_ESCAPE]:
            exit()

        if buttons[pygame.K_LEFT]:
            self.angle -= PLAYER_ROTATE_SPEED
        if buttons[pygame.K_RIGHT]:
            self.angle += PLAYER_ROTATE_SPEED

        if buttons[pygame.K_a]:
            dx = PLAYER_SPEED * sin_angle
            dy = -PLAYER_SPEED * cos_angle
            self.detect_collision(dx, dy)
        if buttons[pygame.K_d]:
            dx = -PLAYER_SPEED * sin_angle
            dy = PLAYER_SPEED * cos_angle
            self.detect_collision(dx, dy)
        if buttons[pygame.K_w]:
            dx = PLAYER_SPEED * cos_angle
            dy = PLAYER_SPEED * sin_angle
            self.detect_collision(dx, dy)
        if buttons[pygame.K_s]:
            dx = -PLAYER_SPEED * cos_angle
            dy = -PLAYER_SPEED * sin_angle
            self.detect_collision(dx, dy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    self.shot = True

    def mouse(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity

    def get_position(self):
        return self.x, self.y
