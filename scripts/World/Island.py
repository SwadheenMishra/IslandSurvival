import pygame
from scripts.World.Tree import TreeManager

class Island:
    def __init__(self, treeManager):
        self.background = pygame.image.load("assets/World/Island/Island.png")
        self.background = pygame.transform.scale(self.background, (1920 * 4, 1080 * 4))
        self.trees = treeManager

    def render(self, screen, cam_x, cam_y):
        screen.blit(self.background, (-cam_x, -cam_y))
        self.trees.render(screen, cam_x, cam_y)
