import pygame
from Player import Player
from World import World

WIDTH, HEIGHT = 800, 500
DEVMODE = True  # Set to False for normal play

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Island Survival")

player = Player(1920 * 2, 1080 * 2)  # Start somewhere in the world
world = World()
world.generate_trees(50)

running = True
clock = pygame.time.Clock()

# --- Day/Night cycle variables ---
time_of_day = 0.4 # Ranges from 0.0 to 1.0 (looping)
desired_minutes_per_day = 5  # ⏱ 5 real minutes per full cycle
fps = 60
time_speed = 1 / (desired_minutes_per_day * 60 * fps)

overlay = pygame.Surface((WIDTH, HEIGHT))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Handle key input ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.move_up(pygame.K_LSHIFT)
    if keys[pygame.K_s]:
        player.move_down(pygame.K_LSHIFT)
    if keys[pygame.K_a]:
        player.move_left(pygame.K_LSHIFT)
    if keys[pygame.K_d]:
        player.move_right(pygame.K_LSHIFT)

    # --- Update time ---
    time_of_day += time_speed
    if time_of_day > 1.0:
        time_of_day = 0.0

    # --- Calculate overlay alpha for day/night darkness ---
    if time_of_day <= 0.5:
        alpha = int((0.5 - time_of_day) * 2 * 180)  # From night to noon
    else:
        alpha = int((time_of_day - 0.5) * 2 * 180)  # From noon to night

    alpha = max(0, min(180, alpha))  # Clamp to safe range

    # --- Render world and player ---
    cam_x, cam_y = player.get_camera_offset(WIDTH, HEIGHT)
    screen.fill((0, 0, 0))
    world.render(screen, cam_x, cam_y)
    mouse_pos = pygame.mouse.get_pos()
    player.render(screen, (WIDTH // 2, HEIGHT // 2), mouse_pos)

    # --- Draw day/night overlay ---
    overlay.fill((0, 0, 0))
    overlay.set_alpha(alpha)
    screen.blit(overlay, (0, 0))

    # --- Debug info ---
    if DEVMODE:
        hour = int(time_of_day * 24)
        minute = int((time_of_day * 24 * 60) % 60)
        print(f"Player pos: {player.get_pos()}, Time: {hour:02d}:{minute:02d}, Alpha: {alpha}")

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
