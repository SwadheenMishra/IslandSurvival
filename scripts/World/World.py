import pygame
import random
from scripts.Entities.Zombies import Zombie
from scripts.Entities.Tree import Tree
from scripts.Entities.NPC import NPC
from scripts.Entities.Boat import Boat
from scripts.Items.Coin import Coin
from scripts.Items.Logs import Logs
# xmin = 750, ymin = 440; xmax = 6770, ymax = 3790

class WorldManager:
    def __init__(self, screen, hud, player, minutes_per_day=5, fps=60):
        self.screen = screen
        self.localPlayer = player
        self.playerHud = hud
        self.fps = fps
        self.time_of_day = 0.375
        self.minutes_per_day = minutes_per_day
        self.time_speed = 1 / (self.minutes_per_day * 60 * self.fps)
        self.TreeDensity = 50
        self.ZombieDensityRng = random.randint(-5, 5)
        self.ZombieDensity = 15 + self.ZombieDensityRng
        self.ZombieSpawnXmin, self.ZombieSpawnXmax = [[700, 1700], [5770, 6770]]
        self.ZombieSpawnYmin, self.ZombieSpawnYmax = [[390, 1390], [2740, 3790]]
        self.WaterDmg = 5
        self.Zombies = []
        self.Trees = []
        self.Coins = []
        self.Logs = []
        self.Traders = []
        self.Boats = []
        self.Boats.append(Boat(5800, 3500, self.playerHud))
        self.Traders.append(NPC(1920 * 1.8, 1080 * 1.8, self.playerHud))

    def get_zombie_density(self):
        return self.ZombieDensity

    def get_tree_density(self):
        return self.TreeDensity

    def spawn_coin(self, x, y):
        self.Coins.append(Coin(x, y, self.screen))
    
    def spawn_logs(self, x, y):
        self.Logs.append(Logs(x, y, self.screen))

    def update_time(self):
        self.time_of_day += self.time_speed
        if self.time_of_day > 1.0:
            self.time_of_day = 0.0
    
    def spawn_zombies(self):
        CurrentCount = 0
        SpawnCount = 0

        h, m = self.get_time()

        if h != 20 or m != 0:
            return
        
        for zombie in self.Zombies:
            if not zombie.is_alive():
                continue

            CurrentCount += 1
        
        if CurrentCount >= self.get_zombie_density():
            return
        
        SpawnCount = self.ZombieDensity - CurrentCount

        for i in range(SpawnCount):
            ZombieSpawnX = random.choice([random.randint(self.ZombieSpawnXmin[0], self.ZombieSpawnXmin[1]), self.ZombieSpawnXmax[0], self.ZombieSpawnXmax[1]])
            ZombieSpawnY = random.choice([random.randint(self.ZombieSpawnYmin[0], self.ZombieSpawnYmin[1]), self.ZombieSpawnYmax[0], self.ZombieSpawnYmax[1]])
            self.Zombies.append(Zombie(ZombieSpawnX, ZombieSpawnY, self.playerHud))


    def spawn_trees(self):
        CurrentCount = 0
        SpawnCount = 0

        h, m = self.get_time()

        if h != 9 or m != 0:
            return
        
        for tree in self.Trees:
            if not tree.is_alive():
                continue

            CurrentCount += 1
        
        if CurrentCount >= self.get_tree_density():
            return
        
        SpawnCount = self.TreeDensity - CurrentCount

        for i in range(SpawnCount):
            y = random.randint(930, 3270)
            x = random.randint(1550, 6170)
            self.Trees.append(Tree(x, y))

    def player_out_of_bounds(self, player, dt):
        px, py = player.get_pos()

        if px > 6770 or px < 750 or py < 440 or py > 3790:
            player.hurt(self.WaterDmg * dt)

    def get_overlay(self):
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.overlay = pygame.Surface((self.width, self.height))
        
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

    def update(self, dt, screen, camX, camY, mousePos, MB1DOWN):
        self.update_time()
        self.player_out_of_bounds(self.localPlayer, dt)

        self.spawn_zombies()
        self.spawn_trees()

        for zombie in self.Zombies:
            zombie.update(screen, self.localPlayer, dt, camX, camY, mousePos, self)
        
        for tree in self.Trees:
            tree.update(screen, self.localPlayer, camX, camY, mousePos, self)

        for coin in self.Coins:
            coin.update(camX, camY, self.localPlayer, self)
        
        for log in self.Logs:
            log.update(camX, camY, self.localPlayer, self)

        for trader in self.Traders:
            trader.update(screen, self.localPlayer, camX, camY, mousePos, MB1DOWN)
        
        for boat in self.Boats:
            boat.update(screen, self.localPlayer, camX, camY, mousePos, MB1DOWN)