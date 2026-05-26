import pygame

from game.camera import Camera, world_to_screen
from game.settings import (
    BG_COLOR,
    DEBUG_PLAYER_SPEED,
    FPS_CAP,
    GRID_MAJOR_COLOR,
    GRID_MAJOR_EVERY,
    GRID_MINOR_COLOR,
    GRID_SPACING,
    WINDOW_H,
    WINDOW_W,
)


Vec2 = pygame.math.Vector2


def draw_world_grid(screen: pygame.Surface, camera: Camera) -> None:
    half_w = WINDOW_W / 2
    half_h = WINDOW_H / 2

    # Visible world rect (with a small margin so lines don't pop).
    world_left = camera.pos.x - half_w - GRID_SPACING
    world_right = camera.pos.x + half_w + GRID_SPACING
    world_top = camera.pos.y - half_h - GRID_SPACING
    world_bottom = camera.pos.y + half_h + GRID_SPACING

    start_x = int(world_left // GRID_SPACING) * GRID_SPACING
    end_x = int(world_right // GRID_SPACING + 1) * GRID_SPACING
    start_y = int(world_top // GRID_SPACING) * GRID_SPACING
    end_y = int(world_bottom // GRID_SPACING + 1) * GRID_SPACING

    major_step = GRID_SPACING * GRID_MAJOR_EVERY

    x = start_x
    while x <= end_x:
        is_major = (x % major_step) == 0
        color = GRID_MAJOR_COLOR if is_major else GRID_MINOR_COLOR
        a = world_to_screen(Vec2(x, world_top), camera, WINDOW_W, WINDOW_H)
        b = world_to_screen(Vec2(x, world_bottom), camera, WINDOW_W, WINDOW_H)
        pygame.draw.line(screen, color, a, b, 2 if is_major else 1)
        x += GRID_SPACING

    y = start_y
    while y <= end_y:
        is_major = (y % major_step) == 0
        color = GRID_MAJOR_COLOR if is_major else GRID_MINOR_COLOR
        a = world_to_screen(Vec2(world_left, y), camera, WINDOW_W, WINDOW_H)
        b = world_to_screen(Vec2(world_right, y), camera, WINDOW_W, WINDOW_H)
        pygame.draw.line(screen, color, a, b, 2 if is_major else 1)
        y += GRID_SPACING

    # World origin marker (0,0) helps verify scrolling direction.
    origin = world_to_screen(Vec2(0, 0), camera, WINDOW_W, WINDOW_H)
    pygame.draw.circle(screen, (230, 80, 80), origin, 6)
    pygame.draw.circle(screen, (10, 10, 12), origin, 6, 2)


def main() -> int:
    pygame.init()
    try:
        screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Avocado Shooter")
        clock = pygame.time.Clock()

        # Temporary world-space player position for verifying camera math (Step 2).
        player_pos = Vec2(0, 0)
        camera = Camera(pos=player_pos.copy())

        running = True
        while running:
            dt = clock.tick(FPS_CAP) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            keys = pygame.key.get_pressed()
            move = Vec2(
                (1 if keys[pygame.K_RIGHT] else 0) - (1 if keys[pygame.K_LEFT] else 0),
                (1 if keys[pygame.K_DOWN] else 0) - (1 if keys[pygame.K_UP] else 0),
            )
            if move.length_squared() > 0:
                move = move.normalize()
                player_pos += move * DEBUG_PLAYER_SPEED * dt

            camera.pos = player_pos

            screen.fill(BG_COLOR)
            draw_world_grid(screen, camera)

            # Player stays centered visually.
            center = Vec2(WINDOW_W / 2, WINDOW_H / 2)
            pygame.draw.circle(screen, (120, 230, 160), center, 10)
            pygame.draw.circle(screen, (10, 10, 12), center, 10, 2)

            pygame.display.flip()
    finally:
        pygame.quit()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
