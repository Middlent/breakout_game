import pygame
import math
import numpy

from managers import Game_Manager
from color import *

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
        # Right movement
        if self.move_right and not self.move_left:
            self.rect.left += self.speed
            if self.rect.colliderect(self.limit_right): # Right limiter colision
                self.rect.right = self.limit_right.left

        # Left movement
        if self.move_left and not self.move_right:
            self.rect.left -= self.speed
            if self.rect.colliderect(self.limit_left): # Left limiter colision
                self.rect.left = self.limit_left.right

        if self.rect.colliderect(Game_Manager.ball.rect):
            if Game_Manager.ball.rect.left < self.rect.left + self.rect.width/3:
                Game_Manager.ball.bounce(self.rect, Ball.COLLISION_UP, Ball.COLLISION_MODE_FORCE_LEFT)
            elif Game_Manager.ball.rect.left > self.rect.left + 3 * self.rect.width/3:
                Game_Manager.ball.bounce(self.rect, Ball.COLLISION_UP, Ball.COLLISION_MODE_FORCE_RIGHT)
            else:
                Game_Manager.ball.bounce(self.rect, Ball.COLLISION_UP)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, BLUE, self.limit_left)
        pygame.draw.rect(screen, BLUE, self.limit_right)

class Bricks():
    def __init__(self):
        pass

class Brick():
    def __init__(self, color, pos):
        pass

class Ball():
    COLLISION_UP = 0
    COLLISION_RIGHT = 1
    COLLISION_DOWN = 2
    COLLISION_LEFT = 3

    COLLISION_MODE_INVERT = 0
    COLLISION_MODE_MAINTAIN = 1
    COLLISION_MODE_FORCE_LEFT = 2
    COLLISION_MODE_FORCE_RIGHT = 3
    def __init__(self):
        self.rect = pygame.rect.Rect(0.5 * Game_Manager.screen_width,
                            0.5 * Game_Manager.screen_height, 
                            0.01 * Game_Manager.screen_width, 
                            0.01 * Game_Manager.screen_height)
        

        self.speed = 0.003 * Game_Manager.screen_width
        self.angle = 60

        self.speed_h = 0
        self.speed_v = 0

        Game_Manager.draw[1].append(self.draw)
        Game_Manager.process.append(self.process)

    def process(self):
        self.speed_h = math.sin(math.radians(self.angle)) * self.speed
        self.speed_v = math.cos(math.radians(self.angle)) * self.speed

        self.rect.y += self.speed_h
        self.rect.x += self.speed_v
    
    def bounce(self, collider, collision_side, collision_mode = 1):
        if collision_side == Ball.COLLISION_UP:
            self.rect.bottom = collider.top
        elif collision_side == Ball.COLLISION_RIGHT:
            self.rect.left = collider.right
            self.angle -= 180 # Adjust for the side collision to work like the top and down collisions
        elif collision_side == Ball.COLLISION_DOWN:
            self.rect.top = collider.bottom
        elif collision_side == Ball.COLLISION_LEFT:
            self.rect.right = collider.left
            self.angle -= 180 # Adjust for the side collision to work like the top and down collisions

        if collision_mode == Ball.COLLISION_MODE_FORCE_LEFT:
            if(numpy.sign(self.speed_h) == 1):
                collision_mode = Ball.COLLISION_MODE_INVERT
            else:
                collision_mode = Ball.COLLISION_MODE_MAINTAIN
        elif collision_mode == Ball.COLLISION_MODE_FORCE_RIGHT:
            if(numpy.sign(self.speed_h) == 1):
                collision_mode = Ball.COLLISION_MODE_MAINTAIN
            else:
                collision_mode = Ball.COLLISION_MODE_INVERT

        if collision_mode == Ball.COLLISION_MODE_INVERT:
            self.angle -= 180
        elif collision_mode == Ball.COLLISION_MODE_MAINTAIN:
            self.angle *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)