import pygame
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, WHITE, BLUE

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        
        # Draw a triangle ship with thrusters
        ship_points = [(20, 0), (0, 40), (40, 40)]  # Triangle
        pygame.draw.polygon(self.image, BLUE, ship_points)
        pygame.draw.polygon(self.image, WHITE, ship_points, 2)  # White outline
        
        # Add thrusters
        pygame.draw.rect(self.image, WHITE, (13, 35, 5, 5))
        pygame.draw.rect(self.image, WHITE, (22, 35, 5, 5))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        
        # Add lives
        self.lives = 3
        self.invulnerable = False
        self.invulnerable_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED

        # Handle invulnerability
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.image.set_alpha(255)
            else:
                # Make ship blink when invulnerable
                alpha = 255 if (self.invulnerable_timer // 4) % 2 else 128
                self.image.set_alpha(alpha)

    def hit(self):
        if not self.invulnerable:
            self.lives -= 1
            if self.lives > 0:
                self.invulnerable = True
                self.invulnerable_timer = 120  # 2 seconds at 60 FPS
            return True
        return False

    def reset_position(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10 