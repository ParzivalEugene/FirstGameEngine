# Основной файл игры где происходит сборка всех модулей в игру

from game_settings import *
import pygame
from player import Player
from sprites import *
from ray_cast import ray_castings_walls
from streaming import Streaming
from music import *
from interaction import Interaction

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
mini_map = pygame.Surface(MINI_MAP_RES)

time = pygame.time.Clock()
sprites = SpriteTypes()
player = Player(sprites)
stream = Streaming(screen, mini_map, player)
interaction = Interaction(player, sprites, stream)

audio = Music()
audio.play(0.4)

while True:
    player.move()

    stream.draw_background(player.angle)
    walls, shot = ray_castings_walls(player, stream.textures)
    stream.draw_environment(walls + [obj.object_locate(player) for obj in sprites.sprites])
    stream.check_fps(time)
    # stream.draw_mini_map(player)
    stream.player_weapon([shot, sprites.sprite_shot()])

    interaction.interact_to_objects()
    interaction.npc_action()
    interaction.delete_trash()

    pygame.display.flip()
    time.tick(FRAMES_PER_SECOND)
