import pygame
from src.sprites.player import Player
from src.sprites.bullet import Bullet
from src.sprites.enemy import Enemy
from src.screens.menu import Menu
from src.constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Galaga Clone")
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen)
        self.score = 0
        self.level = 1
        self.game_state = "MENU"
        self.player = None  # Initialize player reference
        
        # Create small version of player ship for lives display
        self.life_image = pygame.Surface((20, 20), pygame.SRCALPHA)
        ship_points = [(10, 0), (0, 20), (20, 20)]
        pygame.draw.polygon(self.life_image, BLUE, ship_points)
        pygame.draw.polygon(self.life_image, WHITE, ship_points, 1)

        self.red_ratio = 8
        self.yellow_ratio = 2

    def calculate_enemy_count(self):
        # Calculate base enemy count for current level
        count = BASE_ENEMY_COUNT + (self.level - 1) * ENEMY_INCREMENT
        # Double enemy count every ENEMY_DOUBLE_LEVEL levels
        multiplier = 2 ** (self.level // ENEMY_DOUBLE_LEVEL)
        return count * multiplier

    def calculate_enemy_ratios(self):
        total_enemies = self.calculate_enemy_count()
        
        # Calculate green enemies (starting from level 5)
        green_count = 0
        if self.level >= 5:
            green_count = 2 + 2 * ((self.level - 5) // 5)
        
        # Base yellow count is 20% of remaining enemies
        remaining_enemies = total_enemies - green_count
        base_yellow = int(remaining_enemies * 0.2)
        
        # Add 2 more yellow enemies every 2 levels
        additional_yellow = (self.level - 1) // 2 * 2
        
        # Total yellow enemies
        yellow_count = base_yellow + additional_yellow
        
        # Remaining enemies are red
        red_count = total_enemies - yellow_count - green_count
        
        # Ensure we don't have negative red enemies
        if red_count < 0:
            red_count = 0
            # Adjust yellow count if necessary
            yellow_count = total_enemies - green_count
            if yellow_count < 0:
                yellow_count = 0
                green_count = total_enemies
            
        return red_count, yellow_count, green_count

    def draw_lives(self):
        for i in range(self.player.lives):
            self.screen.blit(self.life_image, (10 + 30*i, 40))

    def draw_hud(self):
        font = pygame.font.Font(None, 36)
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        # Draw level
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
        # Draw enemy count
        enemy_text = font.render(f"Enemies: {len(self.enemies)}", True, WHITE)
        self.screen.blit(enemy_text, (SCREEN_WIDTH - 150, 40))
        # Draw lives
        self.draw_lives()

    def new_game(self):
        self.level = 1
        self.score = 0
        # Create new player only when starting a new game
        self.player = Player()
        self.start_level()

    def start_level(self):
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Add existing player to sprites
        self.all_sprites.add(self.player)
        self.player.reset_position()

        # Get enemy counts based on ratios
        red_count, yellow_count, green_count = self.calculate_enemy_ratios()
        
        # Spawn enemies of each type
        for _ in range(red_count):
            self.spawn_enemy('red')
        for _ in range(yellow_count):
            self.spawn_enemy('yellow')
        for _ in range(green_count):
            self.spawn_enemy('green')

    def spawn_enemy(self, enemy_type='random'):
        enemy = Enemy(enemy_type)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def run(self):
        running = True
        while running:
            if self.game_state == "MENU" or self.game_state == "GAME_OVER":
                self.menu.score = self.score
                self.menu.draw(self.game_state == "GAME_OVER")
                action = self.menu.handle_input()
                
                if action == "START":
                    self.game_state = "PLAYING"
                    self.new_game()
                elif action == "QUIT":
                    running = False

            elif self.game_state == "PLAYING":
                self.clock.tick(60)
                
                # Process events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)

                # Update
                self.all_sprites.update()

                # Check for bullet-enemy collisions
                hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
                for hit in hits:
                    self.score += hit.points  # Use enemy-specific point value

                # Check for level completion
                if len(self.enemies) == 0:
                    self.level += 1
                    self.start_level()

                # Check for player-enemy collisions
                hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
                if hits:
                    if self.player.hit():  # Returns True if player actually lost a life
                        if self.player.lives <= 0:
                            self.game_state = "GAME_OVER"
                        else:
                            self.player.reset_position()

                # Draw
                self.screen.fill(BLACK)
                self.all_sprites.draw(self.screen)
                self.draw_hud()
                pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 