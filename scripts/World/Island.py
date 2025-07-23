import pygame

class Island:
    def __init__(self):
        self.background = pygame.image.load("assets/World/Island/Island.png")
        self.background = pygame.transform.scale(self.background, (1920 * 4, 1080 * 4))

    def render(self, screen, cam_x, cam_y):
        screen.blit(self.background, (-cam_x, -cam_y))
