import pygame
from managers import Game_Manager
from color import BLUE

class Player():
    def __init__(self):
        self.rect = pygame.rect.Rect(0.5 * Game_Manager.screen_width,
                            0.9 * Game_Manager.screen_height, 
                            0.05 * Game_Manager.screen_width, 
                            0.02 * Game_Manager.screen_height)
        
        self.limit_left = pygame.rect.Rect(0 * Game_Manager.screen_width,
                            0.9 * Game_Manager.screen_height, 
                            0.02 * Game_Manager.screen_width, 
                            0.02 * Game_Manager.screen_height)
        
        self.limit_right = pygame.rect.Rect(0.98 * Game_Manager.screen_width,
                            0.9 * Game_Manager.screen_height, 
                            0.02 * Game_Manager.screen_width, 
                            0.02 * Game_Manager.screen_height)

        self.speed = 0.01 *Game_Manager.screen_width
        self.move_left = False
        self.move_right = False
        
        Game_Manager.draw[1].append(self.draw)
        Game_Manager.event.append(self.event)
        Game_Manager.process.append(self.process)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left = True
            if event.key == pygame.K_RIGHT:
                self.move_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left = False
            if event.key == pygame.K_RIGHT:
                self.move_right = False

    def process(self):
        if self.move_right and not self.move_left:
            self.rect.left += self.speed
        if self.move_left and not self.move_right:
            self.rect.left -= self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, BLUE, self.limit_left)
        pygame.draw.rect(screen, BLUE, self.limit_right)