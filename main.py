from pathlib import Path

import pygame

from game.camera import Camera, screen_to_world, world_to_screen
from game.settings import (
    BG_COLOR,
    FPS_CAP,
    GRID_MAJOR_COLOR,
    GRID_MAJOR_EVERY,
    GRID_MINOR_COLOR,
    GRID_SPACING,
    PLAYER_SPEED,
    PLAYER_SPRITE_PATH,
    PLAYER_SPRITE_SIZE,
    WINDOW_H,
    WINDOW_W,
)


Vec2 = pygame.math.Vector2


def load_player_sprite() -> tuple[pygame.Surface, pygame.Surface]:
    source_path = Path(PLAYER_SPRITE_PATH)
    if not source_path.is_file():
        raise FileNotFoundError(f"Could not find hero sprite: {source_path}")

    source = pygame.image.load(str(source_path)).convert_alpha()
    right_facing = pygame.transform.scale(source, PLAYER_SPRITE_SIZE)
    left_facing = pygame.transform.flip(right_facing, True, False)
    return right_facing, left_facing


def draw_player_sprite(
    screen: pygame.Surface,
    center: Vec2,
    aim_dir: Vec2,
    sprite_right: pygame.Surface,
    sprite_left: pygame.Surface,
) -> None:
    sprite = sprite_right if aim_dir.x >= 0 else sprite_left
    rect = sprite.get_rect(center=(center.x, center.y + 8))
    screen.blit(sprite, rect)


def draw_gunpoint(screen: pygame.Surface, mouse_pos: Vec2) -> None:
    pygame.draw.circle(screen, (250, 230, 90), mouse_pos, 8, 2)
    pygame.draw.circle(screen, (255, 140, 20), mouse_pos, 3)
    pygame.draw.line(screen, (255, 170, 40), (mouse_pos.x - 12, mouse_pos.y), (mouse_pos.x - 5, mouse_pos.y), 2)
    pygame.draw.line(screen, (255, 170, 40), (mouse_pos.x + 5, mouse_pos.y), (mouse_pos.x + 12, mouse_pos.y), 2)
    pygame.draw.line(screen, (255, 170, 40), (mouse_pos.x, mouse_pos.y - 12), (mouse_pos.x, mouse_pos.y - 5), 2)
    pygame.draw.line(screen, (255, 170, 40), (mouse_pos.x, mouse_pos.y + 5), (mouse_pos.x, mouse_pos.y + 12), 2)


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
        pygame.mouse.set_visible(False)
        player_sprite_right, player_sprite_left = load_player_sprite()

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
                (1 if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) else 0)
                - (1 if (keys[pygame.K_LEFT] or keys[pygame.K_a]) else 0),
                (1 if (keys[pygame.K_DOWN] or keys[pygame.K_s]) else 0)
                - (1 if (keys[pygame.K_UP] or keys[pygame.K_w]) else 0),
            )
            if move.length_squared() > 0:
                move = move.normalize()
                player_pos += move * PLAYER_SPEED * dt

            camera.pos = player_pos

            screen.fill(BG_COLOR)
            draw_world_grid(screen, camera)

            # Player stays centered visually.
            center = Vec2(WINDOW_W / 2, WINDOW_H / 2)
            mouse_screen = Vec2(pygame.mouse.get_pos())
            mouse_world = screen_to_world(mouse_screen, camera, WINDOW_W, WINDOW_H)
            aim = mouse_world - player_pos
            aim_dir = aim.normalize() if aim.length_squared() > 0 else Vec2(1, 0)

            draw_player_sprite(screen, center, aim_dir, player_sprite_right, player_sprite_left)
            draw_gunpoint(screen, mouse_screen)

            pygame.display.flip()
    finally:
        pygame.mouse.set_visible(True)
        pygame.quit()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
