# карта уровня
import pygame
from game_settings import *
from map import map_visualized

LEVEL_WIDTH = len(map_visualized[0]) * CELL
LEVEL_HEIGHT = len(map_visualized) * CELL
level_map, mini_map, walls_collision = {}, set(), []
for j, row in enumerate(map_visualized):
    for i, elem in enumerate(row):
        if elem:
            mini_map.add((i * MAP_CELL, j * MAP_CELL))
            walls_collision.append(pygame.Rect(i * CELL, j * CELL, CELL, CELL))
            level_map[(i * CELL, j * CELL)] = elem
