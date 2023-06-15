import pygame
import random

from pygame.sprite import Sprite
from game.utils.constants import ENEMY_1, ENEMY_2, SCREEN_HEIGHT, SCREEN_WIDTH
from game.components.bullets.bullet import Bullet

class Enemy(Sprite):
    Y_POS = 20
    X_POS_LIST = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    SPEED_X = 5
    SPEED_Y = 1
    MOV_X = {0:'left', 1:'right'}
    IMAGE = {0: ENEMY_1, 1: ENEMY_2}
    
    def __init__(self, image = 1, speed_x = SPEED_X, speed_y = SPEED_Y, move_x_for = [30, 100]):
        self.image = self.IMAGE[image]
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS_LIST[random.randint(0, 10)]
        self.rect.y = self.Y_POS
        self.type = 'enemy'
        
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.movement_x = self.MOV_X[random.randint(0, 1)]
        self.move_x_for = random.randint(move_x_for[0], move_x_for[1])
        self.index = 0
        self.shooting_time = random.randint(30, 50)
        self.shooting_interval = random.randint(1000, 2500)
        self.last_shoot_time = pygame.time.get_ticks() 
    
    def change_movement_x(self):
        self.index += 1
        if (self.index >= self.move_x_for and self.movement_x == 'right') or (self.rect.x >= SCREEN_WIDTH - 40):
            self.movement_x = 'left'
        elif (self.index >= self.move_x_for and self.movement_x == 'left') or (self.rect.x <= 0):
            self.movement_x = 'right'
            
        if self.index >= self.move_x_for:
            self.index = 0
    
    def update(self, ships, game):
        self.rect.y += self.speed_y
        self.shoot(game.bullet_manager)
        
        if self.movement_x == 'left':
            self.rect.x -= self.speed_x
            self.change_movement_x()
        else:
            self.rect.x += self.speed_x
            self.change_movement_x() 
        
        if self.rect.y >= SCREEN_HEIGHT:
            ships.remove(self)
            
    def shoot(self, bullet_manager):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.shooting_interval:
            bullet = Bullet(self)
            bullet_manager.add_bullet(bullet)
            self.last_shoot_time = current_time
    
    def draw(self,  screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
