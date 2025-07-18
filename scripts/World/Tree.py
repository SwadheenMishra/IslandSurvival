import pygame
import random

class TreeManager:
    def __init__(self):
        self.tree1Scale = 100
        self.treeImg1 = pygame.image.load("../assets/World/Tree(s)/Tree1.png")
        self.treeImg1 = pygame.transform.scale(self.treeImg1, (self.tree1Scale, self.tree1Scale))
        self.TreeCoords = []
        self.TreeDensity = 5
        self.generate_trees(self.TreeDensity)

    def generate_trees(self, density: int) -> None:
        for _ in range(density):
            y = random.randint(930, 3270)
            x = random.randint(1550, 6170)
            self.TreeCoords.append((x, y))

    def get_trees(self):
        return self.TreeCoords

    def render(self, screen, cam_x, cam_y):
        for x, y in self.TreeCoords:
            screen.blit(self.treeImg1, (x - cam_x, y - cam_y))