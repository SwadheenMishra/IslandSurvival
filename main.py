import pygame
from scripts.Entities.Player import Player
from scripts.World.Island import Island
from scripts.Render.Hud import Hud
from scripts.World.World import WorldManager
from scripts.Screens.TitleScreen import TitleScreen

# --- Initial Setup ---
WIDTH, HEIGHT = 1920, 1080
# WIDTH, HEIGHT = 850, 540
DEVMODE = False
MouseButton1Down = False

pygame.init()

# Use FULLSCREEN at launch
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Island Survival")

titleScreen = TitleScreen(screen)

# --- World Setup ---
hud = Hud()
player = Player(1920 * 2, 1080 * 2)
world = WorldManager(screen, hud, player, minutes_per_day=5, fps=60)
island = Island()



running = True
clock = pygame.time.Clock()

# --- Time cycle variables ---
time_of_day = 0.4
desired_minutes_per_day = 5
fps = 60
time_speed = 1 / (desired_minutes_per_day * 60 * fps)
dt = 0


# --- Main Loop ---
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            MouseButton1Down = True

        if not titleScreen.MoveToNext and event.type == pygame.MOUSEBUTTONDOWN:
            if titleScreen.play_rect.collidepoint(event.pos):
                player.EntityInCrosshair = True
                if MouseButton1Down:
                    titleScreen.MoveToNext = True  # Start game
            elif titleScreen.quit_rect.collidepoint(event.pos):
                player.EntityInCrosshair = True
                if MouseButton1Down:
                    running = False  # Exit game


        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            MouseButton1Down = False


    if not titleScreen.MoveToNext:
        titleScreen.render()
        hud.render_crosshair(screen, player)
        pygame.display.flip()
        clock.tick(fps)
        dt = clock.get_time() / 1000
        continue

    # --- Input ---
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    # --- Time update ---
    time_of_day += time_speed
    if time_of_day > 1.0:
        time_of_day = 0.0

    # --- Overlay alpha ---
    if time_of_day <= 0.5:
        alpha = int((0.5 - time_of_day) * 2 * 180)
    else:
        alpha = int((time_of_day - 0.5) * 2 * 180)
    alpha = max(0, min(180, alpha))

    # --- World rendering ---
    camX, camY = player.get_camera_offset(screen)
    screen.fill((0, 0, 0))
    island.render(screen, camX, camY)
    world.update(dt, screen, camX, camY, mousePos)
    player.update(screen, mousePos, keys, dt, DEVMODE, MouseButton1Down)

    overlay, alpha = world.get_overlay()
    screen.blit(overlay, (0, 0))

    # --- HUD ---
    hud.render(screen, player, world.Trees, DEVMODE, world)

    if DEVMODE:
        hour, minute = world.get_time()
        print(f"Player pos: {(round(player.get_pos()[0], 1), round(player.get_pos()[1], 1))}, "
              f"Time: {hour:02d}:{minute:02d}, Alpha: {alpha}, "
              f"TimeSinceMoved: {player.get_timeSinceMoved()}")

    pygame.display.flip()
    clock.tick(fps)
    dt = clock.get_time() / 1000

pygame.quit()
