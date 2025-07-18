import pygame

class Hud:
    def __init__(self):
        # Crosshair setup
        self.crosshair = pygame.image.load("../assets/Hud/crosshair/crosshair.png")
        self.crosshair = pygame.transform.scale(self.crosshair, (50, 50))
        pygame.mouse.set_visible(False)

        # Health bar settings
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.stamina_bar_height = 16
        self.bar_spacing = 10

        self.font = pygame.font.SysFont("arial", 16, bold=True)

        # Minimap settings
        self.minimap_size = 150
        self.minimap_border = 5
        self.minimap_scale = 0.03

    def render_crosshair(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        crosshair_rect = self.crosshair.get_rect(center=(mouse_x, mouse_y))
        screen.blit(self.crosshair, crosshair_rect)

    def render_health_bar(self, screen, player):
        self.health = player.get_health()
        bar_x, bar_y = 20, 20

        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, self.health_bar_width, self.health_bar_height), border_radius=4)

        red = int((1 - self.health) * 255)
        green = int(self.health * 255)
        health_color = (red, green, 50)

        current_health_width = int(self.health * self.health_bar_width)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_health_width, self.health_bar_height), border_radius=4)

        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, self.health_bar_width, self.health_bar_height), 2, border_radius=4)

        health_value = int(self.health * 100)
        text_surf = self.font.render(f"{health_value}/100", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(bar_x + self.health_bar_width // 2, bar_y + self.health_bar_height // 2))
        screen.blit(text_surf, text_rect)

    def render_stamina_bar(self, screen, x, y, player):
        stamina = player.get_stamina()

        pygame.draw.rect(screen, (50, 50, 60), (x, y, self.health_bar_width, self.stamina_bar_height), border_radius=4)

        r = int(30 + stamina * 50)
        g = int(100 + stamina * 100)
        b = int(200 + stamina * 55)
        stamina_color = (r, g, b)

        current_stamina_width = int(stamina * self.health_bar_width)
        pygame.draw.rect(screen, stamina_color, (x, y, current_stamina_width, self.stamina_bar_height), border_radius=4)

        pygame.draw.rect(screen, (180, 200, 255), (x, y, self.health_bar_width, self.stamina_bar_height), 2, border_radius=4)

    def render_minimap(self, screen, player, trees, DEVMODE):
        world_x, world_y = player.get_pos()
        size = self.minimap_size

        WORLD_WIDTH = 1920 * 4
        WORLD_HEIGHT = 1080 * 4

        minimap = pygame.Surface((size, size), pygame.SRCALPHA)
        minimap.fill((0, 0, 0, 100))

        scaled_x = int((world_x / WORLD_WIDTH) * size)
        scaled_y = int((world_y / WORLD_HEIGHT) * size)

        pygame.draw.circle(minimap, (255, 255, 255), (scaled_x, scaled_y), 3)

        if DEVMODE:
            for x, y in trees:
                x1, y1 = int((x / WORLD_WIDTH) * size), int((y / WORLD_HEIGHT) * size)
                pygame.draw.circle(minimap, (0, 255, 0), (x1, y1), 3)

        pygame.draw.rect(minimap, (255, 255, 255), (0, 0, size, size), 2)
        screen.blit(minimap, (screen.get_width() - size - 20, 10))
    
    def render_coordinates(self, sceen, player):
        x, y = player.get_pos()
        CoordStr = f"{round(x)}, {round(y)}"
        CoordSurf = self.font.render(CoordStr, True, (255, 255, 255))
        sceen.blit(CoordSurf, (sceen.get_width() - 120 - len(CoordStr), 15 + self.minimap_size))

    def render_time(self, screen, world):
        hour, minute = world.get_time()
        time_string = f"{hour:02d}:{minute:02d}"
        text_surf = self.font.render(f"Time: {time_string}", True, (255, 255, 255))
        screen.blit(text_surf, (20, 20 + self.health_bar_height + self.bar_spacing + self.stamina_bar_height + self.bar_spacing))

    def render(self, screen, player, trees, DEVMODE, world=None):
        self.render_health_bar(screen, player)
        self.render_crosshair(screen)
        self.render_minimap(screen, player, trees, DEVMODE)
        self.render_stamina_bar(screen, 20, 20 + self.health_bar_height + self.bar_spacing, player)
        self.render_time(screen, world)
        self.render_coordinates(screen, player)
