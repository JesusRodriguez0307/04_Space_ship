import pygame
import random
from game.components.enemies.enemy import Enemy
from game.utils.constants import ENEMY_2, SCREEN_HEIGHT, SCREEN_WIDTH

class Enemy2(Enemy):
    def __init__(self):
        super().__init__()
        self.image = ENEMY_2
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS_LIST[random.randint(0, 10)]
        self.rect.y = self.Y_POS
        self.type = 'enemy2'

        self.speed_x = 8
        self.speed_y = 2
        self.move_x_for = random.randint(75, 175)
        
    def change_movement_x(self):
        self.index += 1
        if (self.index >= self.move_x_for and self.movement_x == 'right') or (self.rect.x >= SCREEN_WIDTH - 40):
            self.movement_x = 'left'
        elif (self.index >= self.move_x_for and self.movement_x == 'left') or (self.rect.x <= 0):
            self.movement_x = 'right'
            
        if self.index >= self.move_x_for:
            self.index = 0
    
    def update(self, ships):
        self.rect.y += self.speed_y
        
        if self.movement_x == 'left':
            self.rect.x -= self.speed_x
            self.change_movement_x()
        else:
            self.rect.x += self.speed_x
            self.change_movement_x() 
        
        if self.rect.y >= SCREEN_HEIGHT:
            ships.remove(self)
            
    
    def draw(self,  screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))