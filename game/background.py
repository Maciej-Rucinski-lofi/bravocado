from __future__ import annotations

import random

import pygame

from game.camera import Camera, world_to_screen
from game.settings import (
    MEADOW_BASE_COLOR,
    MEADOW_PATCH_COLOR,
    MEADOW_PATCH_SPACING,
    MEADOW_PATCH_RADIUS,
    MEADOW_FLOWER_COLORS,
    MEADOW_FLOWER_DENSITY,
    TREE_TRUNK_COLOR,
    TREE_CANOPY_COLOR,
    TREE_CANOPY_OUTLINE_COLOR,
    TREE_CELL_SPACING,
    TREE_DENSITY,
    TREE_SCALE_MIN,
    TREE_SCALE_MAX,
    WINDOW_H,
    WINDOW_W,
)


Vec2 = pygame.math.Vector2
WORLD_SEED = random.randint(0, 1_000_000_000)


def _hash2(ix: int, iy: int, salt: int = 0) -> int:
    # Small seeded integer hash to randomize world layout each run.
    n = ix * 374761393 + iy * 668265263 + WORLD_SEED + (salt * 982_451_653)
    n = (n ^ (n >> 13)) * 1274126177
    return n ^ (n >> 16)


def _visible_world_rect(camera: Camera) -> tuple[float, float, float, float]:
    half_w = WINDOW_W / 2
    half_h = WINDOW_H / 2
    return (
        camera.pos.x - half_w,
        camera.pos.x + half_w,
        camera.pos.y - half_h,
        camera.pos.y + half_h,
    )


def draw_meadow(screen: pygame.Surface, camera: Camera) -> None:
    """Draw a simple meadow with trees. Visual-only; no collisions."""
    screen.fill(MEADOW_BASE_COLOR)

    left, right, top, bottom = _visible_world_rect(camera)

    # Soft "grass patches" that stay glued to world-space.
    step = MEADOW_PATCH_SPACING
    start_x = int((left - step) // step)
    end_x = int((right + step) // step) + 1
    start_y = int((top - step) // step)
    end_y = int((bottom + step) // step) + 1

    for ix in range(start_x, end_x):
        for iy in range(start_y, end_y):
            h = _hash2(ix, iy)
            # Roughly 1 in 2 cells gets a patch, but deterministic.
            if (h & 1) == 0:
                continue
            jx = ((h >> 8) & 0xFF) / 255.0 - 0.5
            jy = ((h >> 16) & 0xFF) / 255.0 - 0.5
            center_world = Vec2((ix + 0.5 + jx * 0.7) * step, (iy + 0.5 + jy * 0.7) * step)
            c = world_to_screen(center_world, camera, WINDOW_W, WINDOW_H)
            r = int(MEADOW_PATCH_RADIUS * (0.75 + (((h >> 24) & 0xFF) / 255.0) * 0.7))
            pygame.draw.circle(screen, MEADOW_PATCH_COLOR, (int(c.x), int(c.y)), r)

            # Tiny flowers sprinkled on some patches.
            if MEADOW_FLOWER_DENSITY > 0 and ((h >> 5) % 3) == 0:
                flower_count = int(MEADOW_FLOWER_DENSITY * 10)
                for k in range(flower_count):
                    fk = _hash2(ix * 31 + k * 7, iy * 17 + k * 13)
                    ox = ((fk & 0xFF) / 255.0 - 0.5) * (r * 1.2)
                    oy = (((fk >> 8) & 0xFF) / 255.0 - 0.5) * (r * 1.2)
                    p = Vec2(c.x + ox, c.y + oy)
                    color = MEADOW_FLOWER_COLORS[(fk >> 16) % len(MEADOW_FLOWER_COLORS)]
                    pygame.draw.circle(screen, color, (int(p.x), int(p.y)), 2)

    _draw_trees(screen, camera)


def _draw_trees(screen: pygame.Surface, camera: Camera) -> None:
    left, right, top, bottom = _visible_world_rect(camera)
    step = TREE_CELL_SPACING
    start_x = int((left - step) // step)
    end_x = int((right + step) // step) + 1
    start_y = int((top - step) // step)
    end_y = int((bottom + step) // step) + 1

    for ix in range(start_x, end_x):
        for iy in range(start_y, end_y):
            h = _hash2(ix, iy, salt=17)
            if ((h & 0xFFFF) / 65535.0) > TREE_DENSITY:
                continue

            jx = ((h >> 8) & 0xFF) / 255.0 - 0.5
            jy = ((h >> 16) & 0xFF) / 255.0 - 0.5
            x = (ix + 0.5 + jx * 0.65) * step
            y = (iy + 0.5 + jy * 0.65) * step

            scale_t = ((h >> 24) & 0xFF) / 255.0
            scale = TREE_SCALE_MIN + (TREE_SCALE_MAX - TREE_SCALE_MIN) * scale_t
            base = Vec2(x, y)
            p = world_to_screen(base, camera, WINDOW_W, WINDOW_H)
            trunk_w = int(18 * scale)
            trunk_h = int(42 * scale)
            canopy_r = int(34 * scale)

            trunk = pygame.Rect(int(p.x - trunk_w / 2), int(p.y - trunk_h), trunk_w, trunk_h)
            pygame.draw.rect(screen, TREE_TRUNK_COLOR, trunk, border_radius=max(2, int(4 * scale)))

            canopy_center = (int(p.x), int(p.y - trunk_h))
            pygame.draw.circle(screen, TREE_CANOPY_COLOR, canopy_center, canopy_r)
            pygame.draw.circle(screen, TREE_CANOPY_OUTLINE_COLOR, canopy_center, canopy_r, 2)

