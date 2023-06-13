import pygame
from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH


class Spaceship(Sprite):
    X_POS = (SCREEN_WIDTH // 2) - 40
    Y_POS = 500
    
    def __init__(self):
        self.image = SPACESHIP
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        
    def update(self, user_input):
        if user_input[pygame.K_LEFT]:
            self.move_left()
        elif user_input[pygame.K_RIGHT]:
            self.move_right()
        elif user_input[pygame.K_UP]:
            self.move_up()
        elif user_input[pygame.K_DOWN]:
            self.move_down()

    def move_left(self):
        self.rect.x -= 10
        if self.rect.right <= 0:
            self.rect.x = SCREEN_WIDTH
    
    def move_right(self):
        self.rect.x += 10
        if self.rect.right >=  SCREEN_WIDTH + 50:
            self.rect.x = -self.rect.width
    
    def move_up(self):
        if self.rect.y > SCREEN_HEIGHT // 2:
            self.rect.y -= 10
    
    def move_down(self):
        if self.rect.y < SCREEN_HEIGHT - 70:
            self.rect.y += 10
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))