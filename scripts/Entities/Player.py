import pygame
import time
import math

class Player:
    def __init__(self, x, y):
        self.sprite_scale = 100
        self.originalImage = pygame.image.load("../assets/Player/Axe/PlayerAxe1.png").convert_alpha()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.sprite_scale, self.sprite_scale))
        self.image = self.originalImage
        self.worldX = x
        self.worldY = y
        self.health = 1.0
        self.vel = 200
        self.stamina = 1.0
        self.staminaDec = 0.01
        self.sprintStaminaDec = self.staminaDec * 5
        self.sprintVel = self.vel * 2
        self.slowWalkSpeed = self.vel / 2
        self.TimeWhenMoved = time.time()
        self.TimeSinceMoved = 0

    def get_health(self) -> float:
        return self.health
    
    def get_stamina(self) -> float:
        return self.stamina
    
    def get_pos(self):
        return [self.worldX, self.worldY]
    
    def get_timeSinceMoved(self) -> float:
        return self.TimeSinceMoved

    def render(self, screen, screen_pos, mouse_pos):
        # Calculate angle to mouse
        dx = mouse_pos[0] - screen_pos[0]
        dy = mouse_pos[1] - screen_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))  # y is inverted in pygame

        # Rotate sprite and get new rect centered
        self.image = pygame.transform.rotate(self.originalImage, angle + 90)
        rect = self.image.get_rect(center=screen_pos)

        screen.blit(self.image, rect.topleft)

    # Movement methods (same as before)
    def move_up(self, sprint, dt): 
        v = self.vel
        s = self.staminaDec
        
        if sprint and self.stamina >= self.sprintStaminaDec:
            v = self.sprintVel
            s = self.sprintStaminaDec
        elif self.stamina <= 0:
            v = self.slowWalkSpeed        

        self.worldY -= v * dt
        self.change_stamina(-s, dt)
        self.TimeWhenMoved = time.time()

    def move_down(self, sprint, dt): 
        v = self.vel
        s = self.staminaDec
        
        if sprint and self.stamina >= self.sprintStaminaDec:
            v = self.sprintVel
            s = self.sprintStaminaDec
        elif self.stamina <= 0:
            v = self.slowWalkSpeed       

        self.worldY += v * dt
        self.change_stamina(-s, dt)
        self.TimeWhenMoved = time.time()

    def move_left(self, sprint, dt): 
        v = self.vel
        s = self.staminaDec
        
        if sprint and self.stamina >= self.sprintStaminaDec:
            v = self.sprintVel
            s = self.sprintStaminaDec
        elif self.stamina <= 0:
            v = self.slowWalkSpeed       

        self.worldX -= v * dt
        self.change_stamina(-s, dt)
        self.TimeWhenMoved = time.time()

    def move_right(self, sprint, dt): 
        v = self.vel
        s = self.staminaDec
        
        if sprint and self.stamina >= self.sprintStaminaDec:
            v = self.sprintVel
            s = self.sprintStaminaDec
        elif self.stamina <= 0:
            v = self.slowWalkSpeed      

        self.worldX += v * dt
        self.change_stamina(-s, dt)
        self.TimeWhenMoved = time.time()


    def get_camera_offset(self, screen_w, screen_h):
        return self.worldX - screen_w // 2, self.worldY - screen_h // 2
    
    def hurt(self, amount: float) -> None:
        self.health -= amount

        if self.health < 0:
            self.health = 0
    
    def heal(self, amount: float) -> None:
        self.health += amount

        if self.health > 1.0:
            self.health = 1.0
    
    def change_stamina(self, amount: float, dt: float) -> None:
        self.stamina += amount * dt

        if self.stamina > 1.0:
            self.stamina = 1.0
        elif self.stamina < 0:
            self.stamina = 0

    def regen_stamina(self, dt):
        currentTime = time.time()
        self.TimeSinceMoved = currentTime - self.TimeWhenMoved

        if self.TimeSinceMoved >= 2.5:
            self.change_stamina(0.07, dt)

    def update(self, screen, WIDTH, HEIGHT, mousePos, keys, dt, DEVMODE):
        self.render(screen, (WIDTH // 2, HEIGHT // 2), mousePos)
        self.regen_stamina(dt)

        if keys[pygame.K_w]:
            self.move_up(keys[pygame.K_LSHIFT], dt)
        elif keys[pygame.K_s]:
            self.move_down(keys[pygame.K_LSHIFT], dt)

        if keys[pygame.K_a]:
            self.move_left(keys[pygame.K_LSHIFT], dt)
        elif keys[pygame.K_d]:
            self.move_right(keys[pygame.K_LSHIFT], dt)
        
        if keys[pygame.K_RIGHT]:
            if DEVMODE:
                self.heal(0.01)
        elif keys[pygame.K_LEFT]:
            if DEVMODE:
                self.hurt(0.01)