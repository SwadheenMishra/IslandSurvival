import pygame
from Entities.Player import Player
from World.Island import Island
from Render.Hud import Hud
from World.Tree import TreeManager
from World.World import WorldManager

WIDTH, HEIGHT = 800, 500
DEVMODE = True

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Island Survival")

player = Player(1920 * 2, 1080 * 2)
world = WorldManager(player, WIDTH, HEIGHT, minutes_per_day=5, fps=60)
treeManager = TreeManager()
island = Island(treeManager)
hud = Hud()

running = True
clock = pygame.time.Clock()

# --- Day/Night cycle variables ---
time_of_day = 0.4 # Ranges from 0.0 to 1.0 (looping)
desired_minutes_per_day = 5  # ⏱ 5 real minutes per full cycle
fps = 60
time_speed = 1 / (desired_minutes_per_day * 60 * fps)
dt = 0

overlay = pygame.Surface((WIDTH, HEIGHT))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Handle key input ---
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

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
    camX, camY = player.get_camera_offset(WIDTH, HEIGHT)
    screen.fill((0, 0, 0))
    island.render(screen, camX, camY)
    player.update(screen, WIDTH, HEIGHT, mousePos, keys, dt, DEVMODE)

    # --- Draw day/night overlay ---
    world.update(dt)
    overlay, alpha = world.get_overlay()
    screen.blit(overlay, (0, 0))



    # --- Hud elements ---
    trees = treeManager.get_trees()
    hud.render(screen, player, trees, DEVMODE, world)

    # --- Debug info ---
    if DEVMODE:
        hour, minute = world.get_time()
        print(f"Player pos: {(round(player.get_pos()[0], 1), round(player.get_pos()[1], 1))}, Time: {hour:02d}:{minute:02d}, Alpha: {alpha}, TimeSinceMoved: {player.get_timeSinceMoved()}")

    pygame.display.flip()
    clock.tick(fps)
    dt = clock.get_time() / 1000 

pygame.quit()
