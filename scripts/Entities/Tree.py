import pygame
import random
import time
import math

class Tree:
    def __init__(self, x, y):
        self.sprite_scale = 100
        self.originalImage = pygame.image.load("assets/World/Tree(s)/Tree1.png").convert_alpha()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.sprite_scale, self.sprite_scale))
        self.image = self.originalImage
        self.x = x
        self.y = y
        self.IsAlive = True  # Trees can later be "chopped" if needed
        self.show_health_bar = False
        self.maxHealth = 1.0
        self.health = self.maxHealth
        self.health_bar_timer = 0
        self.health_bar_duration = 2

    def is_alive(self):
        return self.IsAlive

    def get_health(self):
        return self.health

    def get_pos(self):
        return [self.x, self.y]

    def die(self, world):
        for i in range(random.randint(0, 3)):
            XRand, YRand = random.randint(-30, 30), random.randint(-30, 30) 
            world.spawn_logs(self.x + XRand, self.y + YRand)

        self.IsAlive = False

    def distance_from_player(self, player):
        px, py = player.get_pos()
        dx = px - self.x
        dy = py - self.y
        return (dx ** 2 + dy ** 2) ** 0.5

    def check_click(self, mouse_pos, cx, cy, player):
        rect = self.image.get_rect(center=(self.x - cx, self.y - cy))
        if rect.collidepoint(mouse_pos) and (self.distance_from_player(player) < player.get_melee_reach()):
            player.EntityInCrosshair = True

            if player.is_melee_attacking():
                self.hurt(player.get_melee_dmg())

    def render(self, screen, cx, cy):
        rect = self.image.get_rect(center=(self.x - cx, self.y - cy))
        screen.blit(self.image, rect.topleft)

        if self.show_health_bar and time.time() - self.health_bar_timer < self.health_bar_duration:
            bar_width = 40
            bar_height = 6
            health_ratio = max(0, self.health / self.maxHealth)

            bar_x = self.x - cx - bar_width // 2
            bar_y = self.y - cy - self.sprite_scale // 2 - 10

            pygame.draw.rect(screen, (0, 0, 0), (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))

            health_color = (
                int(255 * (1 - health_ratio)),
                int(255 * health_ratio),
                0
            )
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

            font = pygame.font.SysFont("Arial", 10)
            health_text = f"{int(self.health * 100)} / {int(self.maxHealth * 100)}"
            text_surface = font.render(health_text, True, (255, 255, 255))
            screen.blit(text_surface, (bar_x + bar_width // 2 - text_surface.get_width() // 2, bar_y - 12))
        else:
            self.show_health_bar = False

    def update(self, screen, player, cx, cy, mp, world):
        if not self.is_alive():
            return
        self.render(screen, cx, cy)
        self.check_click(mp, cx, cy, player)
        if self.get_health() <= 0:
            self.die(world)

    def hurt(self, amount: float):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.show_health_bar = True
        self.health_bar_timer = time.time()
