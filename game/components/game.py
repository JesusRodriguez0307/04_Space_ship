import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, FONT_STYLE
from game.components.spaceship import Spaceship
from game.components.enemies.enemy_manager import EnemyManager
from game.components.bullets.bullet_manager import BulletManager
from game.components.menu import Menu
from game.components.counter import Counter
from game.components.power_ups.power_up_manager import PowerUpManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() 
        pygame.mixer.music.load("game/assets/Other/soundtrack.mp3")
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.playing = False
        self.game_speed = 10
        
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Spaceship()
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        self.explosion_group = pygame.sprite.Group()
        self.running = False
        self.score_player = Counter()
        self.death_count = Counter()
        self.high_score = Counter()
        self.menu = Menu(self.screen)
        self.power_up_manager = PowerUpManager()
        
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                pygame.mixer.music.play(-1)
                self.show_menu()
        pygame.display.quit()
        pygame.quit()
                
    def run(self):
        self.reset()
        
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            
    def reset(self):
        self.enemy_manager.reset()
        self.score_player.reset()
        self.player.reset()
        self.bullet_manager.reset()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot(self.bullet_manager)
                
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.enemy_manager.update(self)
        self.bullet_manager.update(self)
        self.explosion_group.update()
        self.power_up_manager.update(self)
    
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        
        self.draw_background()
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.explosion_group.draw(self.screen)
        self.score_player.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.power_up_timer()
        
        pygame.display.update()
        pygame.display.flip()
        
    def power_up_timer(self):
        if self.player.has_power_up:
            time_to_show = int(round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2))
            if time_to_show >= 0:
                self.menu.draw(self.screen, f'{self.player.power_up_type.capitalize()} is enabled for {time_to_show} seconds', 500, 50, (255, 255, 255))
    
    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += 10
        
    def show_menu(self):
        self.menu.reset_screen_color(self.screen)
        self.draw_background()
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        
        if self.death_count.count == 0:
            self.menu.draw(self.screen, "Press any key to Start . . .")
        else:
            self.update_higest_score()
            
            self.menu.draw(self.screen, "Game over")
            self.menu.draw(self.screen, f"Score: {self.score_player.count}", half_screen_width, 350)
            self.menu.draw(self.screen, f"highest score: {self.high_score.count}", half_screen_width, 400)
            self.menu.draw(self.screen, f"Deaths: {self.death_count.count}", half_screen_width, 450)

        self.menu.update(self)
     
    def update_higest_score(self):
        if self.score_player.count > self.high_score.count:
            self.high_score.set_count(self.score_player.count)
        