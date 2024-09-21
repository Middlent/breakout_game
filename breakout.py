# library imports
import pygame
import random
import numpy
import math


# local imports
from color import *

pygame.init()

# setting the game screen to the size of the computer screen
info_object = pygame.display.Info()
screen = pygame.display.set_mode((info_object.current_w * 0.9, info_object.current_h * 0.9)) # the <* x>  can be changed to any number to enlarge or shrink the game screen



# game loop
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    pygame.display.flip()
    game_clock.tick(60)

    


pygame.quit()