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

    
    def destroy(self):
        Game_Manager.draw[1].remove(self.draw)
        Game_Manager.event.remove(self.event)
        Game_Manager.process.remove(self.process)

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
            Game_Manager.ball.returning = False
            if Game_Manager.ball.rect.centerx < self.rect.left + 2 * self.rect.width/5:
                Game_Manager.ball.bounce(self.rect, Ball.COLLISION_UP, Ball.COLLISION_MODE_FORCE_LEFT)
            elif Game_Manager.ball.rect.centerx > self.rect.left + 3 * self.rect.width/5:
                Game_Manager.ball.bounce(self.rect, Ball.COLLISION_UP, Ball.COLLISION_MODE_FORCE_RIGHT)
            else:
                Game_Manager.ball.bounce(self.rect, Ball.COLLISION_UP)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, BLUE, self.limit_left)
        pygame.draw.rect(screen, BLUE, self.limit_right)

class Bricks():
    def __init__(self):
        self.bricks = set()
        color = RED
        for i in range(8):
            if i == 2:
                color = ORANGE
            if i == 4:
                color = GREEN
            if i == 6:
                color = YELLOW
            for j in range(14):
                self.bricks.add(Brick(color,(
                    j * (Game_Manager.screen_width * 0.95)/14 + 0.025 * Game_Manager.screen_height,
                    i * 0.025 * Game_Manager.screen_height + 0.2 * Game_Manager.screen_height
                    )))
                
    def destroy(self):
        destroy_queue = []
        for brick in self.bricks:
            destroy_queue.append(brick.destroy)
        for destroy in destroy_queue:
            destroy()

class Brick():
    def __init__(self, color, pos):
        self.color = color
        self.rect = pygame.rect.Rect(pos[0],
                            pos[1], 
                            Game_Manager.screen_width/16, 
                            Game_Manager.screen_height/50)
        
        Game_Manager.draw[1].append(self.draw)
        Game_Manager.process.append(self.process)


    def process(self):
        if self.rect.colliderect(Game_Manager.ball.rect) and not Game_Manager.ball.returning:
            Game_Manager.ball.bounce(self.rect, Ball.COLLISION_DOWN)
            if(Game_Manager.game_started):
                if self.color == YELLOW:
                    Game_Manager.ball.speed += 0.0001 * Game_Manager.screen_width
                    Game_Manager.add_score(1)
                if self.color == GREEN:
                    Game_Manager.ball.speed += 0.0005 * Game_Manager.screen_width
                    Game_Manager.add_score(3)
                if self.color == ORANGE:
                    Game_Manager.ball.speed += 0.0009 * Game_Manager.screen_width
                    Game_Manager.add_score(5)
                if self.color == RED:
                    Game_Manager.ball.speed += 0.0013 * Game_Manager.screen_width
                    Game_Manager.add_score(7)
                Game_Manager.ball.returning = True
                self.destroy()
    
    def destroy(self):
        Game_Manager.draw[1].remove(self.draw)
        Game_Manager.process.remove(self.process)
        Game_Manager.bricks.bricks.remove(self)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    

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

        self.returning = False

        Game_Manager.draw[1].append(self.draw)
        Game_Manager.process.append(self.process)

    def process(self):
        self.speed_v = math.sin(math.radians(self.angle)) * self.speed
        self.speed_h = math.cos(math.radians(self.angle)) * self.speed

        self.rect.y += self.speed_v
        self.rect.x += self.speed_h

        if self.rect.y >= Game_Manager.screen_height:
            Game_Manager.lives -= 1
            self.destroy()
            Game_Manager.ball = Ball()
            if Game_Manager.lives == 0:
                Game_Manager.player.destroy()
                Placeholder()
                Game_Manager.game_started = False
                Game_Manager.bricks.destroy()
                Game_Manager.bricks = Bricks()
                

    def destroy(self):
        Game_Manager.draw[1].remove(self.draw)
        Game_Manager.process.remove(self.process)
    
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

class Placeholder():
    def __init__(self):
        self.rect = pygame.rect.Rect(0,
                            0.9 * Game_Manager.screen_height, 
                            Game_Manager.screen_width, 
                            0.02 * Game_Manager.screen_height)
        
        Game_Manager.draw[1].append(self.draw)
        Game_Manager.event.append(self.event)
        Game_Manager.process.append(self.process)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not Game_Manager.game_started:
                self.destroy()
                Game_Manager.start_game()
                Game_Manager.player = Player()
                Game_Manager.ball.destroy()
                Game_Manager.ball = Ball()
                Game_Manager.score_object.destroy()
                Game_Manager.score_object = Score()
                Game_Manager.bricks.destroy()
                Game_Manager.bricks = Bricks()

        
    def destroy(self):
        Game_Manager.draw[1].remove(self.draw)
        Game_Manager.process.remove(self.process)
        Game_Manager.event.remove(self.event)

    def process(self):
        if self.rect.colliderect(Game_Manager.ball.rect):
            Game_Manager.ball.returning = False
            Game_Manager.ball.bounce(self.rect, Ball.COLLISION_UP)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Score():
    def __init__(self):
        self.score_font = pygame.font.Font('assets/PressStart2P.ttf', 44)
        self.update_score()

        Game_Manager.draw[1].append(self.draw)
    
    def destroy(self):
        Game_Manager.draw[1].remove(self.draw)

    def update_score(self):
        self.score_text = self.score_font.render(str(Game_Manager.score), True, WHITE, BLACK)
        self.score_text_rect = self.score_text.get_rect()
        self.score_text_rect.center = (0.1 * Game_Manager.screen_width,
                            0.1 * Game_Manager.screen_height)

    def draw(self, screen):
        screen.blit(self.score_text, self.score_text_rect)       