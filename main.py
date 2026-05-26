from pathlib import Path

import pygame
from dataclasses import dataclass
import math
import random

from game.camera import Camera, screen_to_world, world_to_screen
from game.background import draw_meadow
from game.settings import (
    BULLET_COLOR,
    BULLET_MUZZLE_OFFSET,
    BULLET_RADIUS,
    BULLET_SPEED,
    BULLET_TTL_MS,
    ENEMY_BODY_COLOR,
    ENEMY_COUNT,
    ENEMY_FACE_COLOR,
    ENEMY_OUTLINE_COLOR,
    ENEMY_RADIUS,
    ENEMY_SPAWN_EXTRA,
    ENEMY_SPAWN_PADDING,
    ENEMY_SPEED,
    FPS_CAP,
    FIRE_INTERVAL_MS,
    CONTACT_DAMAGE,
    CONTACT_DAMAGE_COOLDOWN_MS,
    HP_BAR_H,
    HP_BAR_MARGIN,
    HP_BAR_W,
    GRID_MAJOR_COLOR,
    GRID_MAJOR_EVERY,
    GRID_MINOR_COLOR,
    GRID_SPACING,
    PLAYER_SPEED,
    PLAYER_HP_MAX,
    PLAYER_RADIUS,
    PLAYER_SPRITE_PATH,
    PLAYER_SPRITE_SIZE,
    WINDOW_H,
    WINDOW_W,
)


Vec2 = pygame.math.Vector2


@dataclass
class Bullet:
    pos: Vec2
    vel: Vec2
    born_ms: int


@dataclass
class Enemy:
    pos: Vec2


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


def draw_bullets(screen: pygame.Surface, camera: Camera, bullets: list[Bullet]) -> None:
    for bullet in bullets:
        bullet_screen = world_to_screen(bullet.pos, camera, WINDOW_W, WINDOW_H)
        pygame.draw.circle(
            screen,
            BULLET_COLOR,
            (int(bullet_screen.x), int(bullet_screen.y)),
            BULLET_RADIUS,
        )


def spawn_enemies(player_pos: Vec2, count: int) -> list[Enemy]:
    half_w = WINDOW_W / 2
    half_h = WINDOW_H / 2
    min_radius = math.hypot(half_w, half_h) + ENEMY_SPAWN_PADDING
    max_radius = min_radius + ENEMY_SPAWN_EXTRA

    enemies: list[Enemy] = []
    for _ in range(count):
        angle = random.uniform(0.0, math.tau)
        distance = random.uniform(min_radius, max_radius)
        offset = Vec2(math.cos(angle), math.sin(angle)) * distance
        enemies.append(Enemy(pos=player_pos + offset))
    return enemies


def draw_enemies(screen: pygame.Surface, camera: Camera, enemies: list[Enemy]) -> None:
    for enemy in enemies:
        p = world_to_screen(enemy.pos, camera, WINDOW_W, WINDOW_H)
        cx, cy = int(p.x), int(p.y)
        pygame.draw.circle(screen, ENEMY_BODY_COLOR, (cx, cy), ENEMY_RADIUS)
        pygame.draw.circle(screen, ENEMY_OUTLINE_COLOR, (cx, cy), ENEMY_RADIUS, 2)

        eye_y = cy - int(ENEMY_RADIUS * 0.3)
        eye_dx = int(ENEMY_RADIUS * 0.45)
        eye_r = max(2, int(ENEMY_RADIUS * 0.14))
        pygame.draw.circle(screen, ENEMY_FACE_COLOR, (cx - eye_dx, eye_y), eye_r)
        pygame.draw.circle(screen, ENEMY_FACE_COLOR, (cx + eye_dx, eye_y), eye_r)

        brow_len = int(ENEMY_RADIUS * 0.45)
        brow_drop = int(ENEMY_RADIUS * 0.2)
        pygame.draw.line(
            screen,
            ENEMY_FACE_COLOR,
            (cx - eye_dx - brow_len // 2, eye_y - brow_drop),
            (cx - eye_dx + brow_len // 2, eye_y),
            3,
        )
        pygame.draw.line(
            screen,
            ENEMY_FACE_COLOR,
            (cx + eye_dx - brow_len // 2, eye_y),
            (cx + eye_dx + brow_len // 2, eye_y - brow_drop),
            3,
        )

        mouth_w = int(ENEMY_RADIUS * 1.0)
        mouth_y = cy + int(ENEMY_RADIUS * 0.35)
        pygame.draw.arc(
            screen,
            ENEMY_FACE_COLOR,
            pygame.Rect(cx - mouth_w // 2, mouth_y - 8, mouth_w, 16),
            0.1,
            math.pi - 0.1,
            3,
        )


def draw_hp_bar(screen: pygame.Surface, hp: int, hp_max: int) -> None:
    bar_rect = pygame.Rect(HP_BAR_MARGIN, HP_BAR_MARGIN, HP_BAR_W, HP_BAR_H)
    pygame.draw.rect(screen, (18, 18, 24), bar_rect)
    pygame.draw.rect(screen, (220, 220, 230), bar_rect, 2)

    hp_ratio = 0.0 if hp_max <= 0 else max(0.0, min(1.0, hp / hp_max))
    fill_w = int((HP_BAR_W - 4) * hp_ratio)
    fill_rect = pygame.Rect(HP_BAR_MARGIN + 2, HP_BAR_MARGIN + 2, fill_w, HP_BAR_H - 4)

    if hp_ratio > 0.6:
        fill_color = (72, 210, 100)
    elif hp_ratio > 0.3:
        fill_color = (230, 190, 70)
    else:
        fill_color = (220, 80, 80)
    pygame.draw.rect(screen, fill_color, fill_rect)


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
        bullets: list[Bullet] = []
        enemies = spawn_enemies(player_pos, ENEMY_COUNT)
        last_shot_ms = pygame.time.get_ticks() - FIRE_INTERVAL_MS
        player_hp = PLAYER_HP_MAX
        last_contact_damage_ms = pygame.time.get_ticks() - CONTACT_DAMAGE_COOLDOWN_MS

        running = True
        while running:
            dt = clock.tick(FPS_CAP) / 1000.0
            now_ms = pygame.time.get_ticks()

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

            for enemy in enemies:
                to_player = player_pos - enemy.pos
                if to_player.length_squared() > 0:
                    enemy.pos += to_player.normalize() * ENEMY_SPEED * dt

            camera.pos = player_pos

            draw_meadow(screen, camera)

            # Player stays centered visually.
            center = Vec2(WINDOW_W / 2, WINDOW_H / 2)
            mouse_screen = Vec2(pygame.mouse.get_pos())
            mouse_world = screen_to_world(mouse_screen, camera, WINDOW_W, WINDOW_H)
            aim = mouse_world - player_pos
            aim_dir = aim.normalize() if aim.length_squared() > 0 else Vec2(1, 0)

            if now_ms - last_shot_ms >= FIRE_INTERVAL_MS:
                bullets.append(
                    Bullet(
                        pos=player_pos + (aim_dir * BULLET_MUZZLE_OFFSET),
                        vel=aim_dir * BULLET_SPEED,
                        born_ms=now_ms,
                    )
                )
                last_shot_ms = now_ms

            alive_bullets: list[Bullet] = []
            for bullet in bullets:
                bullet.pos += bullet.vel * dt
                if now_ms - bullet.born_ms <= BULLET_TTL_MS:
                    alive_bullets.append(bullet)
            bullets = alive_bullets

            killed_enemy_ids: set[int] = set()
            killed_bullet_ids: set[int] = set()
            bullet_hit_radius = BULLET_RADIUS + ENEMY_RADIUS
            bullet_hit_radius_sq = bullet_hit_radius * bullet_hit_radius
            for enemy in enemies:
                enemy_id = id(enemy)
                for bullet in bullets:
                    bullet_id = id(bullet)
                    if bullet_id in killed_bullet_ids:
                        continue
                    if (bullet.pos - enemy.pos).length_squared() <= bullet_hit_radius_sq:
                        killed_enemy_ids.add(enemy_id)
                        killed_bullet_ids.add(bullet_id)
                        break
            enemies = [enemy for enemy in enemies if id(enemy) not in killed_enemy_ids]
            bullets = [bullet for bullet in bullets if id(bullet) not in killed_bullet_ids]

            touching_enemy = any(
                (enemy.pos - player_pos).length_squared() <= (ENEMY_RADIUS + PLAYER_RADIUS) ** 2 for enemy in enemies
            )
            if touching_enemy and now_ms - last_contact_damage_ms >= CONTACT_DAMAGE_COOLDOWN_MS:
                player_hp = max(0, player_hp - CONTACT_DAMAGE)
                last_contact_damage_ms = now_ms

            draw_bullets(screen, camera, bullets)
            draw_enemies(screen, camera, enemies)
            draw_player_sprite(screen, center, aim_dir, player_sprite_right, player_sprite_left)
            draw_gunpoint(screen, mouse_screen)
            draw_hp_bar(screen, player_hp, PLAYER_HP_MAX)

            pygame.display.flip()
    finally:
        pygame.mouse.set_visible(True)
        pygame.quit()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
