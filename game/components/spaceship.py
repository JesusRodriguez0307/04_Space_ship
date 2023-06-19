import pygame
from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH
from game.components.bullets.bullet import Bullet
from game.components.bullets.bullet_manager import BulletManager


class Spaceship(Sprite):
    X_POS = (SCREEN_WIDTH // 2) - 40
    Y_POS = 500
    
    def __init__(self):
        self.image = SPACESHIP
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.type = 'player'
        self.last_shot_time = 0
        self.shoot_interval = 5000 
        self.bullet_manager = BulletManager()
        self.has_power_up = False
        self.power_up_type = ''
        self.power_up_time = 0
        self.bullets_per_shot = 3
        pygame.mixer.init()
        self.shoot_sound = pygame.mixer.Sound("game/assets/Other/shoot.wav")
        self.shoot_sound.set_volume(0.3)
        
        
    def update(self, user_input):
        if user_input[pygame.K_LEFT]:
            self.move_left()
        elif user_input[pygame.K_RIGHT]:
            self.move_right()
        elif user_input[pygame.K_UP]:
            self.move_up()
        elif user_input[pygame.K_DOWN]:
            self.move_down()
            
    def shoot(self, bullet_manager):
        self.shoot_sound.play() 
        bullet = Bullet(self)
        bullet_manager.add_bullet(bullet)
        if self.power_up_type == 'Machine Gun' and self.power_up_time > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.shoot_interval:
                bullet = Bullet(self)
                bullet_manager.add_bullet(bullet)
                self.last_shot_time = current_time
                self.shoot(self.bullet_manager)
        # if self.power_up_type == 'Machine Gun' and self.power_up_time > 0:
        #     bullet_offset = self.rect.width // (self.bullets_per_shot - 1)
        #     start_x = self.rect.x - (bullet_offset * (self.bullets_per_shot - 1) // 2)

        #     for i in range(self.bullets_per_shot):
        #         bullet = Bullet(self)
        #         bullet.rect.x = start_x + bullet_offset * i
        #         bullet_manager.add_bullet(bullet)


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
        
    def set_image(self, size, image):
        self.image = image
        self.image = pygame.transform.scale(self.image, size)
    
    def reset(self):
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.has_power_up = False
        self.power_up_type = ''
        self.power_up_time = 0