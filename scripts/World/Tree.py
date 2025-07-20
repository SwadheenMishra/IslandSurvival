import pygame
import random
from scripts.World.World import WorldManager

class TreeManager:
    def __init__(self, world):
        self.tree1Scale = 100
        self.treeImg1 = pygame.image.load("assets/World/Tree(s)/Tree1.png")
        self.treeImg1 = pygame.transform.scale(self.treeImg1, (self.tree1Scale, self.tree1Scale))
        self.TreeCoords = []
        self.generate_trees(world.get_tree_density())

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