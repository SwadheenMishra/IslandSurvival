import pygame

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen

        self.bgImage = pygame.image.load("assets/Hud/MainMenu/BG/TitleScreen.png")

        # Load button images
        self.play_img = pygame.image.load("assets/Hud/MainMenu/Buttons/Play.png").convert_alpha()
        self.quit_img = pygame.image.load("assets/Hud/MainMenu/Buttons/Quit.png").convert_alpha()

        # Resize buttons if needed
        self.play_img = pygame.transform.scale(self.play_img, (200, 200))
        self.quit_img = pygame.transform.scale(self.quit_img, (200, 200))

        self.render()

        self.MoveToNext = False

    def render(self):
        window_width, window_height = self.screen.get_size()

        # Scale and draw background
        scaled_bg = pygame.transform.scale(self.bgImage, (window_width, window_height))
        self.screen.blit(scaled_bg, (0, 0))

        # Dynamically resize buttons (e.g., 1/5th width, maintain aspect ratio)
        button_width = window_width // 6
        button_height = button_width  # square buttons
        self.scaled_play_img = pygame.transform.scale(self.play_img, (button_width, button_height))
        self.scaled_quit_img = pygame.transform.scale(self.quit_img, (button_width, button_height))

        # Position buttons on right side with padding
        margin = 50
        play_x = window_width - button_width - margin
        play_y = window_height // 3
        quit_x = play_x
        quit_y = play_y + button_height + 10  # vertical spacing

        self.play_rect = self.scaled_play_img.get_rect(topleft=(play_x, play_y))
        self.quit_rect = self.scaled_quit_img.get_rect(topleft=(quit_x, quit_y))

        # Draw scaled buttons
        self.screen.blit(self.scaled_play_img, self.play_rect)
        self.screen.blit(self.scaled_quit_img, self.quit_rect)
