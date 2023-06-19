import pygame
import random

from game.components.power_ups.shield import Shield
from game.components.power_ups.machine_gun import MachineGun
from game.utils.constants import SPACESHIP_SHIELD, SPACESHIP, SPACESHIP_MACHINE_GUN

class PowerUpManager:
    def __init__(self):
        pygame.mixer.init()
        self.power_ups = []
        self.when_appears = random.randint(5000, 10000)
        self.duration = random.randint(3, 5)
        self.pick_up_shield = pygame.mixer.Sound("game/assets/Other/pick_up_shield.wav")
        self.pick_up_machine = pygame.mixer.Sound("game/assets/Other/pick_up_machine.wav")

        
    def generate_power_ups(self):
        control = random.randint(0, 1)
        if control == 0:
            power_up = Shield()
        elif control == 1:
            power_up = MachineGun()
        self.when_appears += random.randint(5000, 10000)
        self.power_ups.append(power_up)
        
    def update(self, game):
        current_time = pygame.time.get_ticks()
        
        if len(self.power_ups) == 0 and current_time >= self.when_appears:
            self.generate_power_ups()
            
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            
            if game.player.rect.colliderect(power_up):
                game.player.has_power_up = True
                
                if power_up.type == 'shield':
                    self.pick_up_shield.play()
                    power_up.start_time = pygame.time.get_ticks()
                    game.player.power_up_type = 'Shield'
                    game.player.power_up_time = power_up.start_time + (self.duration * 1000)
                    game.player.set_image((65,75), SPACESHIP_SHIELD)
                    self.power_ups.remove(power_up)
                elif power_up.type == 'machine_gun':
                    power_up.start_time = pygame.time.get_ticks()
                    game.player.power_up_type = 'Machine Gun'
                    game.player.power_up_time = power_up.start_time + (self.duration * 1000)
                    game.player.set_image((40,60), SPACESHIP_MACHINE_GUN)
                    self.power_ups.remove(power_up)
                
            if current_time >= power_up.start_time + (self.duration * 1000):
                game.player.power_up_type = ''
                game.player.power_up_time = 0
                game.player.set_image((40,60), SPACESHIP)
                
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
            
    def reset(self):
        self.power_ups = []
        self.when_appears = random.randint(5000, 10000)
