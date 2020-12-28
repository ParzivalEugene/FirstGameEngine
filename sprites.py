from game_settings import *
import pygame
from collections import deque
from ray_cast import mapping


class SpriteTypes:
    def __init__(self):
        self.sprite_parameters = {
            'npc_cacodemon': {
                'sprite': [pygame.image.load('textures/sprites/cocodemon/static/'
                                             f'{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.0,
                'scale': (1.1, 1.1),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'textures/sprites/cocodemon/death/{i}.'
                                                            'png').convert_alpha()
                                          for i in range(6)]),
                'is_dead': False,
                'dead_shift': 0.6,
                'animation_dist': 1000,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'npc',
                'action': deque([pygame.image.load('textures/sprites/cocodemon/animation/'
                                                 f'{i}.png').convert_alpha() for i in range(9)])
            },
            'decor_flame': {
                'sprite': pygame.image.load('textures/sprites/flame/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': (0.6, 0.6),
                'side': 30,
                'animation': deque(
                    [pygame.image.load(f'textures/sprites/flame/{i}.png').convert_alpha() for i in
                     range(16)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 1.8,
                'animation_dist': 1000,
                'animation_speed': 5,
                'blocked': None,
                'flag': 'decor',
                'action': []
            },
            'vertical_door': {
                'sprite': [pygame.image.load('textures/sprites/doors/vertical_doors/'
                                             f'{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': False,
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'horizontal_door',
                'action': []
            },
            'horizontal_door': {
                'sprite': [pygame.image.load('textures/sprites/doors/horizontal_doors/'
                                             f'{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': False,
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'vertical_door',
                'action': []
            }
        }
        self.sprites = [
            SpriteObjects(self.sprite_parameters['horizontal_door'], (8.5, 3.5)),
            SpriteObjects(self.sprite_parameters['horizontal_door'], (5.5, 8.5)),
            SpriteObjects(self.sprite_parameters['horizontal_door'], (14.5, 17.5)),
            SpriteObjects(self.sprite_parameters['npc_cacodemon'], (15, 16)),
        ]
        # self.sprites = [
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (7, 5)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (7, 6)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (7, 8)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (7, 7)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (7, 9)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (7, 11)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (7, 13)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (7, 15)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (9, 5)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (9, 7)),
        #     SpriteObjects(self.sprite_parameters['npc_cacodemon'], (9, 11)),
        #     SpriteObjects(self.sprite_parameters['decor_flame'], (5, 2.5)),
        #     SpriteObjects(self.sprite_parameters['vertical_door'], (2.5, 6.5)),
        #     SpriteObjects(self.sprite_parameters['vertical_door'], (9.5, 4.5)),
        #     SpriteObjects(self.sprite_parameters['vertical_door'], (11.5, 4.5)),
        #     SpriteObjects(self.sprite_parameters['horizontal_door'], (10.5, 3.5)),
        #     SpriteObjects(self.sprite_parameters['horizontal_door'], (10.5, 5.5)),
        # ]

    def sprite_shot(self):
        return min([obj.is_on_line() for obj in self.sprites], default=(float('inf'), 0))

    def blocked_doors(self):
        blocked_doors = {}
        for obj in self.sprites:
            if obj.flag in {'vertical_door', 'horizontal_door'} and obj.blocked:
                i, j = mapping(obj.x, obj.y)
                blocked_doors[(i, j)] = 0
        return blocked_doors


class SpriteObjects:
    def __init__(self, parameters, pos):
        self.x, self.y = pos[0] * CELL, pos[1] * CELL

        self.object = parameters['sprite'].copy()
        self.viewing_angle = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()

        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']

        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.side = parameters['side']
        self.flag = parameters['flag']
        self.action = parameters['action'].copy()
        self.dead_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_previous_position = self.y if self.flag == 'horizontal_door' else self.x
        self.delete = False

        if self.viewing_angle:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 360)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 360)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_position = {angle: pos for angle, pos in
                                    zip(self.sprite_angles, self.object)}

    def is_on_line(self):
        if CENTRAL_RAY - self.side // 2 < self.ray < CENTRAL_RAY + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.projection_height
        return float('inf'), None

    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = sqrt(dx ** 2 + dy ** 2)

        self.alpha = atan2(dy, dx)
        beta = self.alpha - player.angle
        if dx > 0 and 180 <= degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            beta += DOUBLE_PI
        self.alpha -= 1.4 * beta

        delta_rays = int(beta / DELTA_OF_ANGLE)
        self.ray = CENTRAL_RAY + delta_rays
        if self.flag not in {'vertical_door', 'horizontal_door'}:
            self.distance_to_sprite *= cos(HALF_FIELD_OF_VIEW - self.ray * DELTA_OF_ANGLE)

        additional_ray = self.ray + ADDITIONAL_RAYS
        if 0 <= additional_ray <= ADDITIONAL_RAYS_RANGE and self.distance_to_sprite > 30:
            self.projection_height = min(int(COEFFICIENT / self.distance_to_sprite),
                                         DOUBLE_HEIGHT if self.flag not in {'vertical_door',
                                                                            'horizontal_door'}
                                         else HEIGHT)
            sprite_width = int(self.projection_height * self.scale[0])
            sprite_height = int(self.projection_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            if self.flag in {'vertical_door', 'horizontal_door'}:
                if self.door_open_trigger:
                    self.open_door()
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()
            else:
                if self.is_dead and self.is_dead != 'immortal':
                    sprite_object = self.dead_animation()
                    shift = half_sprite_height * self.dead_shift
                    sprite_height = int(sprite_height / 1.3)
                elif self.npc_action_trigger:
                    sprite_object = self.npc_in_action()
                else:
                    self.object = self.visible_sprite()
                    sprite_object = self.sprite_animation()
            sprite_position = (self.ray * SCALE - half_sprite_width,
                               HALF_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return self.distance_to_sprite, sprite, sprite_position
        else:
            return (False,)

    def sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        if self.viewing_angle:
            if self.alpha < 0:
                self.alpha += DOUBLE_PI
            alpha = 360 - int(degrees(self.alpha))

            for angles in self.sprite_angles:
                if alpha in angles:
                    return self.sprite_position[angles]
        return self.object

    def dead_animation(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    def npc_in_action(self):
        sprite_object = self.action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.action.rotate()
            self.animation_count = 0
        return sprite_object

    def open_door(self):
        if self.flag == 'horizontal_door':
            self.y -= 3
            if abs(self.y - self.door_previous_position) > CELL:
                self.delete = True
        elif self.flag == 'vertical_door':
            self.x -= 3
            if abs(self.x - self.door_previous_position) > CELL:
                self.delete = True
