import pygame
import random
import time
import math

class NPC:
    def __init__(self, x, y):
        self.sprite_scale = 100
        self.originalImage = pygame.image.load("assets/Entities/Trader/Trader.png").convert_alpha()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.sprite_scale, self.sprite_scale))
        self.image = self.originalImage
        self.x = x
        self.y = y

    def is_alive(self):
        return self.IsAlive

    def get_health(self):
        return self.health

    def get_pos(self):
        return [self.x, self.y]

    def distance_from_player(self, player):
        px, py = player.get_pos()
        dx = px - self.x
        dy = py - self.y
        return (dx ** 2 + dy ** 2) ** 0.5

    def OpenTradeMenu():
        pass 
    
    def check_click(self, mouse_pos, cx, cy, player):
        rect = self.image.get_rect(center=(self.x - cx, self.y - cy))
        if rect.collidepoint(mouse_pos) and (self.distance_from_player(player) < player.get_melee_reach()):
            player.EntityInCrosshair = True

            if player.is_melee_attacking():
                self.OpenTradeMenu()

    def render(self, screen, cx, cy):
        rect = self.image.get_rect(center=(self.x - cx, self.y - cy))
        screen.blit(self.image, rect.topleft)

    def update(self, screen, player, cx, cy, mp):
        if not self.is_alive():
            return
        self.render(screen, cx, cy)
        self.check_click(mp, cx, cy, player)