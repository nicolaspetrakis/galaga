import pygame
from ..constants import YELLOW, BULLET_SPEED

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 16), pygame.SRCALPHA)
        
        # Draw energy bolt
        pygame.draw.line(self.image, YELLOW, (2, 0), (2, 16), 4)
        # Add glow effect
        pygame.draw.line(self.image, (255, 255, 200), (2, 0), (2, 16), 2)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill() 