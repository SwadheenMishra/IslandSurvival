import pygame

class Boat:
    def __init__(self, x, y, hud):
        self.sprite_scale = 200
        self.originalImage = pygame.image.load("assets/World/Boat/BoatDmg.png").convert_alpha()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.sprite_scale, self.sprite_scale))
        self.image = self.originalImage
        self.PlayerHud = hud
        self.x = x
        self.y = y

    def get_pos(self):
        return [self.x, self.y]

    def distance_from_player(self, player):
        px, py = player.get_pos()
        dx = px - self.x
        dy = py - self.y
        return (dx ** 2 + dy ** 2) ** 0.5
    
    def check_click(self, mouse_pos, cx, cy, player):
        rect = self.image.get_rect(center=(self.x - cx, self.y - cy))

        if (self.distance_from_player(player) < player.get_melee_reach()):
            if rect.collidepoint(mouse_pos):
                player.EntityInCrosshair = True

                if player.is_melee_attacking():
                    if player.HasPart:
                        player.Won = True
        else:
            pass
            # exit repair screen code

    def render(self, screen, cx, cy):
        rect = self.image.get_rect(center=(self.x - cx, self.y - cy))
        screen.blit(self.image, rect.topleft)

    def update(self, screen, player, cx, cy, mp, MB1DOWN):
        self.render(screen, cx, cy)
        self.check_click(mp, cx, cy, player)

        # CODE TO OPEN REPAIR SCREEN
        MB1DOWN