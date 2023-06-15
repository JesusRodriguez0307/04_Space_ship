import pygame
from pygame.sprite import Sprite
from game.utils.constants import EXPLOSION

class Explosion(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = EXPLOSION
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_speed = 50
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        
        self.scale_factor = 0.5
        self.images = [pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor))) for image in self.images]
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.current_frame]
                
    def draw(self, screen):
        screen.blit(self.image, self.rect)