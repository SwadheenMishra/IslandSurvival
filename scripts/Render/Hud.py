import pygame

class Hud:
    def __init__(self):
        # Crosshair setup
        self.orignalCrosshairScale = 50
        self.crosshairExpandMultiplier = 1.5
        self.BigCrosshairScale = self.orignalCrosshairScale * self.crosshairExpandMultiplier
        self.ResourceIconScale = 55
        self.LogIcon = pygame.image.load("assets/World/Items/Logs/LogIcon.png")
        self.CoinsIcon = pygame.image.load("assets/World/Items/Coin/Coin.png")
        self.crosshairImg = pygame.image.load("assets/Hud/crosshair/crosshair.png")
        self.LogIcon = pygame.transform.scale(self.LogIcon, (self.ResourceIconScale, self.ResourceIconScale))
        self.CoinsIcon = pygame.transform.scale(self.CoinsIcon, (self.ResourceIconScale, self.ResourceIconScale))
        self.crosshair = pygame.transform.scale(self.crosshairImg, (self.orignalCrosshairScale, self.orignalCrosshairScale))
        
        pygame.mouse.set_visible(False)

        # Health bar settings
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.stamina_bar_height = 16
        self.bar_spacing = 10

        self.font = pygame.font.Font("assets/Hud/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 12)
        self.DeathFont = pygame.font.Font("assets/Hud/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 70)
        self.ResourceFont = pygame.font.Font("assets/Hud/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 25)

        # Minimap settings
        self.minimap_size = 150
        self.minimap_border = 5
        self.minimap_scale = 0.03

    def render_crosshair(self, screen, player):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if player.EntityInCrosshair: 
            self.crosshair = pygame.transform.scale(
                self.crosshairImg,
                (self.BigCrosshairScale, self.BigCrosshairScale)
            )
        else:
            self.crosshair = pygame.transform.scale(
                self.crosshairImg,
                (self.orignalCrosshairScale, self.orignalCrosshairScale)
            )
        
        crosshair_rect = self.crosshair.get_rect(center=(mouse_x, mouse_y))
        screen.blit(self.crosshair, crosshair_rect)

        player.EntityInCrosshair = False

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

    def render_minimap(self, screen, player, trees, zombies, logs, coins, DEVMODE):
        world_x, world_y = player.get_pos()
        size = self.minimap_size

        WORLD_WIDTH = 1920 * 4
        WORLD_HEIGHT = 1080 * 4

        minimap = pygame.Surface((size, size), pygame.SRCALPHA)
        minimap.fill((0, 0, 0, 100))

        scaled_x = int((world_x / WORLD_WIDTH) * size)
        scaled_y = int((world_y / WORLD_HEIGHT) * size)

        if DEVMODE:
            for tree in trees:
                if not tree.is_alive():
                    continue

                xt, yt = tree.get_pos()
                x1, y1 = int((xt / WORLD_WIDTH) * size), int((yt / WORLD_HEIGHT) * size)
                pygame.draw.circle(minimap, (0, 255, 0), (x1, y1), 3)
            for zombie in zombies:
                if not zombie.is_alive():
                    continue
                
                xz, yz = zombie.get_pos()
                x2, y2 = int((xz / WORLD_WIDTH) * size), int((yz / WORLD_HEIGHT) * size)
                pygame.draw.circle(minimap, (255, 0, 0), (x2, y2), 3)

            for log in logs:
                xl, yl = log.get_pos()
                x3, y3 = int((xl / WORLD_WIDTH) * size), int((yl / WORLD_HEIGHT) * size)
                pygame.draw.circle(minimap, (150, 75, 0), (x3, y3), 3)

            for coin in coins:
                xc, yc = coin.get_pos()
                x4, y4 = int((xc / WORLD_WIDTH) * size), int((yc / WORLD_HEIGHT) * size)
                pygame.draw.circle(minimap, (255, 215, 0), (x4, y4), 3)


        pygame.draw.circle(minimap, (255, 255, 255), (scaled_x, scaled_y), 3)
        pygame.draw.rect(minimap, (255, 255, 255), (0, 0, size, size), 2)
        screen.blit(minimap, (screen.get_width() - size - 20, 10))
    
    def render_coordinates(self, sceen, player):
        x, y = player.get_pos()
        CoordStr = f"{round(x)}, {round(y)}"
        CoordSurf = self.font.render(CoordStr, True, (255, 255, 255))
        sceen.blit(CoordSurf, (sceen.get_width() - 148 - len(CoordStr), 15 + self.minimap_size))
    
    def render_resources(self, screen, player):
        LogsStr = f"x{player.Logs}"
        LogsTxt = self.ResourceFont.render(LogsStr, True, (255, 255, 255))

        CoinStr = f"x{player.Coins}"
        CoinTxt = self.ResourceFont.render(CoinStr, True, (255, 255, 255))

        total_width = LogsTxt.get_width()
        y = 20
        x = (screen.get_width() - total_width) // 2

        screen.blit(self.LogIcon, (x - 130, y - 15))
        screen.blit(LogsTxt, (x - 60, y))
        screen.blit(self.CoinsIcon, (x + 80, y - 15))
        screen.blit(CoinTxt, (x + 140, y))

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
        self.render_crosshair(screen, player)
        self.render_minimap(screen, player, trees, world.Zombies, world.Logs, world.Coins, DEVMODE)
        self.render_stamina_bar(screen, 20, 20 + self.health_bar_height + self.bar_spacing, player)
        self.render_time(screen, world)
        self.render_coordinates(screen, player)
        self.render_resources(screen, player)