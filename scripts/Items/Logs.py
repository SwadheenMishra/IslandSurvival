import pygame

class Logs:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.scale = 50
        self.image = pygame.image.load("assets/World/Items/Logs/Logs.png")
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
    
    def get_pos(self):
        return [self.x, self.y]

    def distance_from_player(self, player):
        px, py = player.get_pos()
        x, y = self.get_pos()
        dx = px - x
        dy = py - y
        return (dx ** 2 + dy ** 2) ** 0.5
    
    def render(self, camX, camY):
        screen_x = self.x - camX
        screen_y = self.y - camY
        rect = self.image.get_rect(center=(screen_x, screen_y))
        self.screen.blit(self.image, rect.topleft)
    
    def despawn(self, world):
        if self in world.Logs:
            world.Logs.remove(self)

    def check_pickup(self, player, world):
        if self.distance_from_player(player) <= 40:
            player.Logs += 1
            self.despawn(world)
    
    def update(self, camX, camY, player, world):
        self.render(camX, camY)
        self.check_pickup(player, world)