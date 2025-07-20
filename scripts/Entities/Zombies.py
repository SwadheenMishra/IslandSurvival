import pygame
import time
import math

class Zombie:
    def __init__(self, x, y, hud):
        self.sprite_scale = 100
        self.originalImage = pygame.image.load("assets/Entities/Zombie/Zombie1.png").convert_alpha()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.sprite_scale, self.sprite_scale))
        self.image = self.originalImage
        self.speed = 150
        self.maxHealth = 0.5
        self.attackDmg = 0.1
        self.health = self.maxHealth
        self.IsAlive = True
        self.sightRange = 600
        self.AttackReach = 100
        self.attackCoolDown = 2
        self.TimeWhenAttacked = time.time()
        self.TimeSinceAttacked = 0
        self.x = x
        self.y = y
        self.show_health_bar = False
        self.health_bar_timer = 0
        self.health_bar_duration = 2
        self.PlayerHud = hud
        self.Angry = False
        self.Attack = False

    def get_attack_reach(self):
        return self.AttackReach

    def is_angry(self):
        return self.Angry

    def get_sight_range(self):
        return self.sightRange

    def is_alive(self) -> bool:
        return self.IsAlive

    def get_health(self) -> float:
        return self.health
    
    def get_pos(self):
        return [self.x, self.y]
    
    def die(self):
        self.IsAlive = False

    def distance_from_player(self, player):
        px, py = player.get_pos()
        dx = px - self.x
        dy = py - self.y
        return (dx ** 2 + dy ** 2) ** 0.5


    def check_click(self, mouse_pos, cx, cy, dt, player):
        rect = self.image.get_rect(center=(self.x - cx, self.y - cy))
        if rect.collidepoint(mouse_pos) and (self.distance_from_player(player) < player.get_melee_reach()):
            self.PlayerHud.crosshair = pygame.transform.scale(self.PlayerHud.crosshair, (self.PlayerHud.BigCrosshairScale, self.PlayerHud.BigCrosshairScale))
            if player.is_melee_attacking():
                self.hurt(player.get_melee_dmg())
        else:
            self.PlayerHud.crosshair = pygame.transform.scale(self.PlayerHud.crosshair, (self.PlayerHud.orignalCrosshairScale, self.PlayerHud.orignalCrosshairScale))


    def render(self, screen, cx, cy, player, angry):
        if angry:
            px, py = player.get_pos()
            dx = px - self.x
            dy = py - self.y
            angle = math.degrees(math.atan2(-dy, dx))
            self.image = pygame.transform.rotate(self.originalImage, angle + 90)

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

    def attack(self, target):
        if self.TimeSinceAttacked >= self.attackCoolDown:
            target.hurt(self.attackDmg)
            self.TimeWhenAttacked = time.time()


    def move(self, player, dt):
        px, py = player.get_pos()
        dx = px - self.x
        dy = py - self.y
        distance = math.hypot(dx, dy)

        if distance == 0:
            return  # Prevent division by zero

        # Normalize direction vector
        dx /= distance
        dy /= distance

        # Move zombie
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt


    def hurt(self, amount: float) -> None:
        self.health -= amount

        if self.health < 0:
            self.health = 0

        self.show_health_bar = True
        self.health_bar_timer = time.time()

    def heal(self, amount: float) -> None:
        self.health += amount

        if self.health > 1.0:
            self.health = 1.0

    def update(self, screen, player, dt, cx, cy, mp):
        if not self.is_alive():
            return
        
        if not player.is_alive():
            return
        
        distanceFromPlayer = self.distance_from_player(player) 
        self.Angry = distanceFromPlayer <= self.get_sight_range()
        self.TimeSinceAttacked = time.time() - self.TimeWhenAttacked

        if self.is_angry():
            self.move(player, dt)
            if distanceFromPlayer <= self.get_attack_reach():
                self.attack(player)

        self.render(screen, cx, cy, player, self.is_angry())
        self.check_click(mp, cx, cy, dt, player)

        if self.get_health() <= 0:
            self.die()