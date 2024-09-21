# library imports
import pygame
import random
import numpy
import math


# local imports
from color import WHITE, BLACK
from managers import Game_Manager
from entities import Player

pygame.init()

# setting the game screen to the size of the computer screen
# every size and position have to be a value from 0 to 1 multiplied by screen heigth or width
info_object = pygame.display.Info()
screen = pygame.display.set_mode((0.4 * info_object.current_w, 0.8 * info_object.current_h))
Game_Manager.update_screen_size()

player = Player()

# sets size and position for left wall and add it to the draw queue
wall_left = pygame.rect.Rect(0 * Game_Manager.screen_width,
                            0 * Game_Manager.screen_height, 
                            0.02 * Game_Manager.screen_width, 
                            1 * Game_Manager.screen_height)
Game_Manager.draw[0].append(lambda screen : pygame.draw.rect(screen,WHITE, wall_left))

# sets size and position for right wall and add it to the draw queue
wall_right = pygame.rect.Rect(0.98 * Game_Manager.screen_width,
                            0 * Game_Manager.screen_height, 
                            0.02 * Game_Manager.screen_width, 
                            1 * Game_Manager.screen_height)
Game_Manager.draw[0].append(lambda screen : pygame.draw.rect(screen,WHITE, wall_right))

# sets size and position for top wall and add it to the draw queue
wall_top = pygame.rect.Rect(0 * Game_Manager.screen_width,
                            0 * Game_Manager.screen_height, 
                            1 * Game_Manager.screen_width, 
                            0.05 * Game_Manager.screen_height)
Game_Manager.draw[0].append(lambda screen : pygame.draw.rect(screen,WHITE, wall_top))


# game loop
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:
    screen.fill(BLACK)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
        for event_func in Game_Manager.event:
            event_func(event)

    for draw in Game_Manager.draw[0]:
        draw(screen)
    for draw in Game_Manager.draw[1]:
        draw(screen)

    for process in Game_Manager.process:
        process()

    pygame.display.flip()
    game_clock.tick(60)

    


pygame.quit()