import pygame
import time
import math

class Player:
    def __init__(self, x, y):
        self.sprite_scale = 100
        self.originalImage = pygame.image.load("assets/Entities/Player/Axe/PlayerAxe1.png").convert_alpha()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.sprite_scale, self.sprite_scale))
        self.Axe3Image = pygame.image.load("assets/Entities/Player/Axe/PlayerAxe3.png").convert_alpha()
        self.Axe3Image = pygame.transform.scale(self.Axe3Image, (self.sprite_scale, self.sprite_scale))
        self.image = self.originalImage
        self.worldX = x
        self.worldY = y
        self.maxHealth = 1
        self.health = self.maxHealth
        self.vel = 200
        self.staminaRegenTime = 2.5
        self.stamina = 1.0
        self.staminaDec = 0.01
        self.sprintStaminaDec = self.staminaDec * 5
        self.sprintVel = self.vel * 2
        self.slowWalkSpeed = self.vel / 2
        self.TimeWhenMoved = time.time()
        self.TimeSinceMoved = 0
        self.attackCoolDown = 1
        self.TimeWhenAttacked = 0
        self.TimeSinceAttacked = 0
        self.IsAlive = True
        self.MeleeDmg = 0.3
        self.GunDmg = 0.5
        self.StartingCoins = 0
        self.StartingLogs = 0
        self.Coins = self.StartingCoins
        self.Logs = self.StartingLogs
        self.meleeReach = 130
        self.maleeAttacking = False
        self.EntityInCrosshair = False
        self.IsTrading = False
        self.HasBinoculars = False
        self.HasPart = False
        self.HasGun = False
        self.Won = False

    def get_stamina_regen_time(self):
        return self.staminaRegenTime

    def get_melee_reach(self):
        return self.meleeReach

    def get_max_health(self):
        return self.maxHealth

    def is_melee_attacking(self):
        return self.maleeAttacking

    def get_melee_dmg(self) -> float:
        return self.MeleeDmg
    
    def get_gun_dmg(self) -> float:
        return self.GunDmg

    def is_alive(self) -> bool:
        return self.IsAlive

    def get_health(self) -> float:
        return self.health

    def get_stamina(self) -> float:
        return self.stamina

    def get_pos(self):
        return [self.worldX, self.worldY]

    def get_timeSinceMoved(self) -> float:
        return self.TimeSinceMoved

    def die(self):
        self.IsAlive = False

    def render(self, screen, screen_pos, mouse_pos):
        if (not self.IsTrading) and (not self.Won):
            
            dx = mouse_pos[0] - screen_pos[0]
            dy = mouse_pos[1] - screen_pos[1]
            angle = math.degrees(math.atan2(-dy, dx))

            # Use attack image if currently attacking
            if self.TimeSinceAttacked <= self.attackCoolDown:
                image_to_use = self.Axe3Image 
            else:
                image_to_use = self.originalImage

            self.image = pygame.transform.rotate(image_to_use, angle + 90)
            self.rect = self.image.get_rect(center=screen_pos)

        screen.blit(self.image, self.rect.topleft)

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

    def move(self, keys, dt):
        if keys[pygame.K_w]:
            self.move_up(keys[pygame.K_LSHIFT], dt)
        elif keys[pygame.K_s]:
            self.move_down(keys[pygame.K_LSHIFT], dt)

        if keys[pygame.K_a]:
            self.move_left(keys[pygame.K_LSHIFT], dt)
        elif keys[pygame.K_d]:
            self.move_right(keys[pygame.K_LSHIFT], dt)


    def get_camera_offset(self, screen):
        screen_w, screen_h = screen.get_width(), screen.get_height()
        return self.worldX - screen_w // 2, self.worldY - screen_h // 2

    def hurt(self, amount: float) -> None:
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount: float) -> None:
        self.health += amount
        if self.health > self.get_max_health():
            self.health = self.get_max_health()

    def change_stamina(self, amount: float, dt: float) -> None:
        self.stamina += amount * dt
        if self.stamina > 1.0:
            self.stamina = 1.0
        elif self.stamina < 0:
            self.stamina = 0

    def regen_stamina(self, dt):
        currentTime = time.time()
        self.TimeSinceMoved = currentTime - self.TimeWhenMoved

        if self.TimeSinceMoved >= self.get_stamina_regen_time():
            self.change_stamina(0.07, dt)

    def update(self, screen, mousePos, keys, dt, DEVMODE, MB1DOWN):
        if not self.is_alive():
            return

        self.TimeSinceAttacked = time.time() - self.TimeWhenAttacked

        # Start attack if possible
        if not self.Won:
            if MB1DOWN and self.TimeSinceAttacked >= self.attackCoolDown:
                self.maleeAttacking = True
                self.TimeWhenAttacked = time.time()
            else:
                self.maleeAttacking = False

        self.render(screen, (screen.get_width() // 2, screen.get_height() // 2), mousePos)
        self.regen_stamina(dt)

        if self.get_health() <= 0:
            self.die()

        if (not self.IsTrading) and (not self.Won):
            self.move(keys, dt)

        if keys[pygame.K_RIGHT] and DEVMODE:
            self.heal(0.01)
        elif keys[pygame.K_LEFT] and DEVMODE:
            self.hurt(0.01)
        elif keys[pygame.K_UP] and DEVMODE:
            self.maxHealth += 0.1 * dt
        elif keys[pygame.K_DOWN] and DEVMODE:
            self.maxHealth -= 0.1 * dt
            self.health = self.get_max_health()