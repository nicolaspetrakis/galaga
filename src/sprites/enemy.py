import pygame
import random
import math
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, RED, WHITE, YELLOW, GREEN, ENEMY_SPEED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type='random'):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        # Set enemy type and properties
        if enemy_type == 'random':
            self.enemy_type = random.choice(['red', 'yellow'])
        else:
            self.enemy_type = enemy_type
            
        if self.enemy_type == 'red':
            self.color = RED
            self.speed_multiplier = 0.7  # Slower
            self.points = 10
        elif self.enemy_type == 'yellow':
            self.color = YELLOW
            self.speed_multiplier = 1.5  # Faster
            self.points = 20
        else:  # green
            self.color = GREEN
            self.speed_multiplier = 1.0
            self.points = 30
            # Circular movement properties
            self.angle = random.uniform(0, 2 * math.pi)
            self.radius = random.randint(30, 50)
            self.circle_speed = random.uniform(0.05, 0.1)
            self.base_x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
            self.vertical_speed = random.uniform(1, 2)
        
        # Draw the ship based on type
        if self.enemy_type == 'green':
            # Diamond shape for green ships
            points = [(15, 0), (30, 15), (15, 30), (0, 15)]
            pygame.draw.polygon(self.image, self.color, points)
            pygame.draw.polygon(self.image, WHITE, points, 1)
        else:
            # Original ship design for red and yellow
            pygame.draw.ellipse(self.image, self.color, (5, 10, 20, 15))
            pygame.draw.ellipse(self.image, WHITE, (5, 10, 20, 15), 1)
            
            top_points = [(15, 5), (8, 12), (22, 12)]
            pygame.draw.polygon(self.image, self.color, top_points)
            pygame.draw.polygon(self.image, WHITE, top_points, 1)
            
            pygame.draw.polygon(self.image, self.color, [(2, 15), (8, 15), (5, 25)])
            pygame.draw.polygon(self.image, self.color, [(22, 15), (28, 15), (25, 25)])
            pygame.draw.polygon(self.image, WHITE, [(2, 15), (8, 15), (5, 25)], 1)
            pygame.draw.polygon(self.image, WHITE, [(22, 15), (28, 15), (25, 25)], 1)
        
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        if self.enemy_type == 'green':
            self.rect.centerx = self.base_x
            self.rect.centery = -50
            self.current_y = float(self.rect.centery)
        else:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4) * self.speed_multiplier
            self.speedx = random.choice([-1, 1]) * random.randrange(1, 3) * self.speed_multiplier
            self.direction_timer = random.randrange(30, 90)

    def update(self):
        if self.enemy_type == 'green':
            # Update vertical position
            self.current_y += self.vertical_speed
            self.rect.centery = self.current_y
            
            # Calculate circular movement
            self.angle += self.circle_speed
            self.rect.centerx = self.base_x + math.sin(self.angle) * self.radius
            
            # Reset if completely off screen (including horizontal space)
            if self.rect.top > SCREEN_HEIGHT + 50:
                self.reset_position()
        else:
            # Original movement for red and yellow ships
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            
            self.direction_timer -= 1
            if self.direction_timer <= 0:
                self.speedx *= -1
                self.direction_timer = random.randrange(30, 90)
            
            if self.rect.left < 0:
                self.rect.left = 0
                self.speedx *= -1
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                self.speedx *= -1
                
            if self.rect.top > SCREEN_HEIGHT:
                self.reset_position() 