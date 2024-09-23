import pygame

class Game_Manager():
    game_started = False
    score = 0
    lives = 3

    screen_width = 0
    screen_height = 0

    process = []
    draw = [[],[]] # the draw function have 2 layers, the thing on the botton have to be in layer 0, the things on top on layer 1
    event = []

    player = None
    ball = None
    bricks = None
    score_object = None
    

    def start_game():
        Game_Manager.game_started = True
        Game_Manager.score = 0
        Game_Manager.lives = 3

    def add_score(value):
        Game_Manager.score += value
        Game_Manager.score_object.update_score()

    def update_screen_size():
        info = pygame.display.Info()
        Game_Manager.screen_width = info.current_w
        Game_Manager.screen_height = info.current_h