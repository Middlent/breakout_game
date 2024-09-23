import pygame


from managers import Game_Manager
from color import WHITE
from entities import Ball

class Wall_Left():
    def __init__(self):
        self.rect = pygame.rect.Rect(0 * Game_Manager.screen_width,
                            0 * Game_Manager.screen_height, 
                            0.02 * Game_Manager.screen_width, 
                            1 * Game_Manager.screen_height)
        
        Game_Manager.draw[0].append(self.draw)
        Game_Manager.process.append(self.process)


    def process(self):
        if self.rect.colliderect(Game_Manager.ball.rect):
            Game_Manager.ball.bounce(self.rect, Ball.COLLISION_RIGHT)
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Wall_Right():
    def __init__(self):
        self.rect = pygame.rect.Rect(0.98 * Game_Manager.screen_width,
                            0 * Game_Manager.screen_height, 
                            0.02 * Game_Manager.screen_width, 
                            1 * Game_Manager.screen_height)
        
        Game_Manager.draw[0].append(self.draw)
        Game_Manager.process.append(self.process)


    def process(self):
        if self.rect.colliderect(Game_Manager.ball.rect):
            Game_Manager.ball.bounce(self.rect, Ball.COLLISION_LEFT)
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Wall_Top():
    def __init__(self):
        self.rect = pygame.rect.Rect(0 * Game_Manager.screen_width,
                            0 * Game_Manager.screen_height, 
                            1 * Game_Manager.screen_width, 
                            0.05 * Game_Manager.screen_height)
        
        Game_Manager.draw[0].append(self.draw)
        Game_Manager.process.append(self.process)


    def process(self):
        if self.rect.colliderect(Game_Manager.ball.rect):
            Game_Manager.ball.bounce(self.rect, Ball.COLLISION_DOWN)
            Game_Manager.ball.returning = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)