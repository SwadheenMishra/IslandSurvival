import pygame

class Hud:
    def __init__(self):
        # Crosshair setup
        self.orignalCrosshairScale = 50
        self.crosshairExpandMultiplier = 1.5
        self.BigCrosshairScale = self.orignalCrosshairScale * self.crosshairExpandMultiplier
        self.crosshair = pygame.image.load("assets/Hud/crosshair/crosshair.png")
        self.crosshair = pygame.transform.scale(self.crosshair, (self.orignalCrosshairScale, self.orignalCrosshairScale))
        pygame.mouse.set_visible(False)

        # Health bar settings
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.stamina_bar_height = 16
        self.bar_spacing = 10

        self.font = pygame.font.Font("assets/Hud/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 12)
        self.DeathFont = pygame.font.Font("assets/Hud/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 70)

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
        MaxHealth = player.get_max_health()
        bar_x, bar_y = 20, 20

        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, self.health_bar_width, self.health_bar_height), border_radius=4)

        red = int((MaxHealth - self.health) * 255)
        green = int((self.health/MaxHealth) * 255)
        health_color = (red, green, 50)

        current_health_width = int((1 - (MaxHealth - self.health)) * self.health_bar_width)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_health_width, self.health_bar_height), border_radius=4)

        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, self.health_bar_width, self.health_bar_height), 2, border_radius=4)

        text_surf = self.font.render(f"{int(self.health*100)}/{int(MaxHealth*100)}", True, (255, 255, 255))
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

    def render_minimap(self, screen, player, trees, zombies, DEVMODE):
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
            for zombie in zombies:
                if not zombie.is_alive():
                    continue
                
                x, y = zombie.get_pos()
                x2, y2 = int((x / WORLD_WIDTH) * size), int((y / WORLD_HEIGHT) * size)
                pygame.draw.circle(minimap, (255, 0, 0), (x2, y2), 3)

        pygame.draw.rect(minimap, (255, 255, 255), (0, 0, size, size), 2)
        screen.blit(minimap, (screen.get_width() - size - 20, 10))
    
    def render_coordinates(self, sceen, player):
        x, y = player.get_pos()
        CoordStr = f"{round(x)}, {round(y)}"
        CoordSurf = self.font.render(CoordStr, True, (255, 255, 255))
        sceen.blit(CoordSurf, (sceen.get_width() - 148 - len(CoordStr), 15 + self.minimap_size))

    def render_time(self, screen, world):
        hour, minute = world.get_time()
        time_string = f"{hour:02d}:{minute:02d}"
        text_surf = self.font.render(f"Time: {time_string}", True, (255, 255, 255))
        screen.blit(text_surf, (20, 20 + self.health_bar_height + self.bar_spacing + self.stamina_bar_height + self.bar_spacing))

    def render_death_screen(self, screen):
        # Create both parts of the text
        text1 = self.DeathFont.render("You ", True, (255, 255, 255))  # white
        text2 = self.DeathFont.render("died", True, (255, 0, 0))      # red

        # Combine widths
        total_width = text1.get_width() + text2.get_width()
        y = screen.get_height() // 2
        x = (screen.get_width() - total_width) // 2

        # Blit both texts
        screen.blit(text1, (x, y))
        screen.blit(text2, (x + text1.get_width(), y))


    def render(self, screen, player, trees, DEVMODE, world=None):
        if not player.is_alive():
            pygame.mouse.set_visible(True)
            self.render_death_screen(screen)
            return

        self.render_health_bar(screen, player)
        self.render_crosshair(screen)
        self.render_minimap(screen, player, trees, world.Zombies, DEVMODE)
        self.render_stamina_bar(screen, 20, 20 + self.health_bar_height + self.bar_spacing, player)
        self.render_time(screen, world)
        self.render_coordinates(screen, player)