# library imports
import pygame
import random


# local imports
from color import WHITE, BLACK
from managers import Game_Manager
from entities import Player, Ball
from walls import *

pygame.init()

# setting the game screen to the size of the computer screen
# every size and position have to be a value from 0 to 1 multiplied by screen heigth or width
info_object = pygame.display.Info()
screen = pygame.display.set_mode((0.4 * info_object.current_w, 0.8 * info_object.current_h))
Game_Manager.update_screen_size()

Game_Manager.player = Player()
Game_Manager.ball  = Ball()
Wall_Top()
Wall_Left()
Wall_Right()



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