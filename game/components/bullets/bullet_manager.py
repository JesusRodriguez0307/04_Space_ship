import pygame
from game.components.explosion import Explosion

class BulletManager:
    def __init__(self):
        self.bullets = []
        self.enemy_bullets = []
        self.explosion_group = pygame.sprite.Group()
        
    def update(self, game):
        for enemy_bullets in self.enemy_bullets:
            enemy_bullets.update(self.enemy_bullets)
            if enemy_bullets.rect.colliderect(game.player.rect) and enemy_bullets.owner == 'enemy':
                if game.player.power_up_type != 'Shield':
                    game.death_count.update()
                    self.enemy_bullets.remove(enemy_bullets)
                    pygame.time.delay(1000)
                    game.show_menu
                    game.playing = False
                    game.player.reset()
                break
            
        for bullet in self.bullets:
            bullet.update(self.bullets)
            if bullet.owner == 'player':
                self.check_collision(bullet, game.enemy_manager, game)
    
    def check_collision(self, bullet, enemy_manager, game):
        for enemy in enemy_manager.enemies:
            if bullet.rect.colliderect(enemy.rect):
                game.score_player.update()
                self.bullets.remove(bullet)
                enemy_manager.enemies.remove(enemy)
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.explosion_group.add(explosion)
                break
    
    def draw(self, screen):
        for enemy_bullets in self.enemy_bullets:
            enemy_bullets.draw(screen)
        
        for bullet in self.bullets:
            bullet.draw(screen)
        
        self.explosion_group.draw(screen)
        self.explosion_group.update()
            
    def add_bullet(self, bullet):
        if bullet.owner == 'enemy':
            self.enemy_bullets.append(bullet)
        if bullet.owner == 'player':
            self.bullets.append(bullet)
            
    def reset(self):
        self.bullets = []
        self.enemy_bullets = []