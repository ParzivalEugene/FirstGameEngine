from level import level_map
from game_settings import *
from level import LEVEL_HEIGHT, LEVEL_WIDTH
import pygame


def mapping(x, y):
    return (x // CELL) * CELL, (y // CELL) * CELL


def ray_casting(player_pos, player_angle):
    casted_walls = []
    x_start, y_start = player_pos
    x_angle, y_angle = mapping(x_start, y_start)
    current_angle = player_angle - HALF_FIELD_OF_VIEW
    for ray in range(NUMBER_OF_RAYS):
        sin_angle = sin(current_angle)
        sin_angle = sin_angle if sin_angle else 0.000001
        cos_angle = cos(current_angle)
        cos_angle = cos_angle if cos_angle else 0.000001
        horizontal_texture, vertical_texture = 1, 1
        if cos_angle >= 0:
            x, k = x_angle + CELL, 1
        else:
            x, k = x_angle, -1

        for i in range(0, LEVEL_WIDTH, CELL):
            vertical_depth = (x - x_start) / cos_angle
            vertical_y = y_start + vertical_depth * sin_angle
            vertical_tile = mapping(x + k, vertical_y)
            if vertical_tile in level_map:
                vertical_texture = level_map[vertical_tile]
                break
            x += k * CELL

        if sin_angle >= 0:
            y, k = y_angle + CELL, 1
        else:
            y, k = y_angle, -1

        for i in range(0, LEVEL_HEIGHT, CELL):
            horizontal_depth = (y - y_start) / sin_angle
            horizontal_x = x_start + horizontal_depth * cos_angle
            horizontal_tile = mapping(horizontal_x, y + k)
            if horizontal_tile in level_map:
                horizontal_texture = level_map[horizontal_tile]
                break
            y += k * CELL

        depth, offset, texture = (vertical_depth, vertical_y, vertical_texture)\
            if vertical_depth < horizontal_depth \
            else (horizontal_depth, horizontal_x, horizontal_texture)
        offset = int(offset) % CELL
        depth *= cos(player_angle - current_angle)
        depth = max(depth, 0.000001)
        projection_height = int(COEFFICIENT / depth)
        current_angle += DELTA_OF_ANGLE
        casted_walls.append((depth, offset, projection_height, texture))
    return casted_walls


def ray_castings_walls(player, textures):
    walls = []
    casted_walls = ray_casting(player.get_position(), player.angle)
    shot = casted_walls[CENTRAL_RAY][0], casted_walls[CENTRAL_RAY][2]
    for ray, values in enumerate(casted_walls):
        depth, offset, projection_height, texture = values
        if projection_height > HEIGHT:
            k = projection_height / HEIGHT
            texture_height = TEXTURE_HEIGHT / k
            wall = textures[texture].subsurface(offset * TEXTURE_SCALE,
                                                HALF_TEXTURE_HEIGHT - texture_height // 2,
                                                TEXTURE_SCALE, texture_height)
            wall = pygame.transform.scale(wall, (SCALE, HEIGHT))
            wall_pos = (ray * SCALE, 0)
        else:
            wall = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE,
                                                TEXTURE_HEIGHT)
            wall = pygame.transform.scale(wall, (SCALE, projection_height))
            wall_pos = (ray * SCALE, HALF_HEIGHT - projection_height // 2)
        walls.append((depth, wall, wall_pos))
    return walls, shot
