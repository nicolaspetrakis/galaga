import pygame
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ["Start Game", "Quit"]

    def draw(self, game_over=False):
        self.screen.fill(BLACK)
        
        # Title
        title = "GALAGA" if not game_over else "Game Over"
        title_surface = self.font_big.render(title, True, WHITE)
        title_rect = title_surface.get_rect(centerx=SCREEN_WIDTH//2, y=100)
        self.screen.blit(title_surface, title_rect)

        # Menu options
        for i, option in enumerate(self.options):
            color = WHITE
            if i == self.selected_option:
                text = f"> {option} <"
            else:
                text = option

            text_surface = self.font_small.render(text, True, color)
            text_rect = text_surface.get_rect(centerx=SCREEN_WIDTH//2, y=300 + i * 50)
            self.screen.blit(text_surface, text_rect)

        if game_over:
            score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(centerx=SCREEN_WIDTH//2, y=200)
            self.screen.blit(score_text, score_rect)

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        return "START"
                    elif self.selected_option == 1:
                        return "QUIT"
        return None 