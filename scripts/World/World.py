import pygame

# xmin = 750, ymin = 440; xmax = 6770, ymax = 3790

class WorldManager:
    def __init__(self, player, width, height, minutes_per_day=5, fps=60):
        self.width = width
        self.height = height
        self.fps = fps
        self.time_of_day = 0.4
        self.minutes_per_day = minutes_per_day
        self.time_speed = 1 / (self.minutes_per_day * 60 * self.fps)
        self.overlay = pygame.Surface((self.width, self.height))
        self.WaterDmg = 5

    def update_time(self):
        self.time_of_day += self.time_speed
        if self.time_of_day > 1.0:
            self.time_of_day = 0.0
    
    def player_out_of_bounds(self, player, dt):
        px, py = player.get_pos()

        if px > 6770 or px < 750 or py < 440 or py > 3790:
            player.hurt(0.1 * dt)

    def get_overlay(self):
        # Day to noon to night transition
        if self.time_of_day <= 0.5:
            alpha = int((0.5 - self.time_of_day) * 2 * 180)
        else:
            alpha = int((self.time_of_day - 0.5) * 2 * 180)

        alpha = max(0, min(180, alpha))  # Clamp
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(alpha)
        return self.overlay, alpha

    def get_time(self):
        hour = int(self.time_of_day * 24)
        minute = int((self.time_of_day * 24 * 60) % 60)
        return hour, minute

    def update(self):
        self.update_time()
        # self.player_out_of_bounds(player, dt)