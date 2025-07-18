import pygame
import math

class Player:
    def __init__(self, x, y):
        self.sprite_scale = 100
        self.original_image = pygame.image.load("../assets/Player/Gun/PlayerGun2.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.sprite_scale, self.sprite_scale))
        self.image = self.original_image
        self.world_x = x
        self.world_y = y
        self.vel = 5
        self.sprintVel = 8

    def get_pos(self):
        return [self.world_x, self.world_y]

    def render(self, screen, screen_pos, mouse_pos):
        # Calculate angle to mouse
        dx = mouse_pos[0] - screen_pos[0]
        dy = mouse_pos[1] - screen_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))  # y is inverted in pygame

        # Rotate sprite and get new rect centered
        self.image = pygame.transform.rotate(self.original_image, angle + 90)
        rect = self.image.get_rect(center=screen_pos)

        screen.blit(self.image, rect.topleft)

    # Movement methods (same as before)
    def move_up(self, sprint): self.world_y -= self.sprintVel if sprint else self.vel
    def move_down(self, sprint): self.world_y += self.sprintVel if sprint else self.vel
    def move_left(self, sprint): self.world_x -= self.sprintVel if sprint else self.vel
    def move_right(self, sprint): self.world_x += self.sprintVel if sprint else self.vel

    def get_camera_offset(self, screen_w, screen_h):
        return self.world_x - screen_w // 2, self.world_y - screen_h // 2
