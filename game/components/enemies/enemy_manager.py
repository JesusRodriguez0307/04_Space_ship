from game.components.enemies.enemy import Enemy
from game.components.enemies.enemy_2 import Enemy2

class EnemyManager:
    def __init__(self):
        self.enemies = []
        
    def update(self):
        self.add_enemy()
        for enemy in self.enemies:
            enemy.update(self.enemies)
        
    def add_enemy(self):
        if len(self.enemies) < 5:
            enemy = Enemy()
            self.enemies.append(enemy)
        
        if len(self.enemies) == 5:
            enemy2 = Enemy2()            
            self.enemies.append(enemy2)
            
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
            