import pygame
from game_settings import *
from level import level_map
from ray_cast import mapping


def ray_casting_npc_player(npc_x, npc_y, blocked_doors, current_map, player_pos):
    x_start, y_start = player_pos
    x_angle, y_angle = mapping(x_start, y_start)
    delta_x, delta_y = x_start - npc_x, y_start - npc_y

    current_angle = atan2(delta_y, delta_x) + pi

    sin_angle = sin(current_angle)
    sin_angle = sin_angle if sin_angle else 0.000001
    cos_angle = cos(current_angle)
    cos_angle = cos_angle if cos_angle else 0.000001
    horizontal_texture, vertical_texture = 1, 1

    x, k = (x_angle + CELL, 1) if cos_angle >= 0 else (x_angle, -1)

    for i in range(0, int(abs(delta_x)) // CELL):
        vertical_depth = (x - x_start) / cos_angle
        vertical_y = y_start + vertical_depth * sin_angle
        vertical_tile = mapping(x + k, vertical_y)
        if vertical_tile in level_map or vertical_tile in blocked_doors:
            return False
        x += k * CELL

    y, k = (y_angle + CELL, 1) if sin_angle >= 0 else (y_angle, -1)
    for i in range(0, int(abs(delta_y)) // CELL):
        horizontal_depth = (y - y_start) / sin_angle
        horizontal_x = x_start + horizontal_depth * cos_angle
        horizontal_tile = mapping(horizontal_x, y + k)
        if horizontal_tile in level_map or horizontal_tile in blocked_doors:
            return False
        y += k * CELL
    return True


class Interaction:
    def __init__(self, player, sprites, streaming):
        self.player = player
        self.sprites = sprites
        self.streaming = streaming
        self.death_sound = pygame.mixer.Sound('sounds/pain.wav')

    def interact_to_objects(self):
        if self.player.shot and self.streaming.shot_animation_trigger:
            for obj in sorted(self.sprites.sprites, key=lambda x: x.distance_to_sprite):
                if obj.is_on_line()[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if obj.flag in {'horizontal_door', 'vertical_door'}:
                            obj.door_open_trigger = True
                            obj.blocked = False
                        if ray_casting_npc_player(obj.x, obj.y, self.sprites.blocked_doors(),
                                                  level_map, self.player.get_position()):
                            if obj.flag == 'npc':
                                self.death_sound.set_volume(0.5)
                                self.death_sound.play()
                            obj.is_dead = True
                            obj.blocked = False
                            self.streaming.shot_animation_trigger = False

                        break

    def npc_action(self):
        for obj in self.sprites.sprites:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y, self.sprites.blocked_doors(),
                                          level_map, self.player.get_position()):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj):
        if abs(obj.distance_to_sprite) > CELL:
            dx = obj.x - self.player.get_position()[0]
            dy = obj.y - self.player.get_position()[1]
            obj.x = obj.x + 1 if dx < 0 else obj.x - 1
            obj.y = obj.y + 1 if dy < 0 else obj.y - 1

    def delete_trash(self):
        deleted = self.sprites.sprites.copy()
        for obj in deleted:
            if obj.delete:
                self.sprites.sprites.remove(obj)
