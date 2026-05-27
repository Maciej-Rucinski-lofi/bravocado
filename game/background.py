from __future__ import annotations

import random
from pathlib import Path

import pygame

from game.camera import Camera, map_half_extents, meadow_half_extents, world_to_screen
from game.settings import (
    GRASS_SPRITE_PATH,
    MAP_BORDER_WIDTH,
    MAP_H,
    MAP_W,
    MUD_BORDER_SPRITE_PATH,
    SPACE_COLOR,
    STAR_CELL_SPACING,
    STAR_DENSITY,
    STAR_FINE_DENSITY,
    STAR_FINE_SPACING,
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
_mud_tile: pygame.Surface | None = None
_grass_tile: pygame.Surface | None = None


def _get_mud_tile() -> pygame.Surface:
    global _mud_tile
    if _mud_tile is None:
        path = Path(MUD_BORDER_SPRITE_PATH)
        if not path.is_file():
            raise FileNotFoundError(f"Could not find mud border sprite: {path}")
        source = pygame.image.load(str(path))
        _mud_tile = pygame.transform.scale(source, (MAP_BORDER_WIDTH, MAP_BORDER_WIDTH))
        if pygame.display.get_surface() is not None:
            _mud_tile = _mud_tile.convert()
    return _mud_tile


def _get_grass_tile() -> pygame.Surface:
    global _grass_tile
    if _grass_tile is None:
        path = Path(GRASS_SPRITE_PATH)
        if not path.is_file():
            raise FileNotFoundError(f"Could not find grass background sprite: {path}")
        _grass_tile = pygame.image.load(str(path))
        if pygame.display.get_surface() is not None:
            _grass_tile = _grass_tile.convert()
    return _grass_tile


def _hash2(ix: int, iy: int, salt: int = 0) -> int:
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


def _point_in_meadow(x: float, y: float, meadow_half: Vec2) -> bool:
    return -meadow_half.x <= x <= meadow_half.x and -meadow_half.y <= y <= meadow_half.y


def draw_scene(screen: pygame.Surface, camera: Camera) -> None:
    """Space background, tiled grass meadow, mud border, trees."""
    _draw_space(screen, camera)
    _draw_grass(screen, camera)
    _draw_mud_border(screen, camera)
    meadow_half = meadow_half_extents(MAP_W, MAP_H, MAP_BORDER_WIDTH)
    _draw_trees(screen, camera, meadow_half)


def _draw_space(screen: pygame.Surface, camera: Camera) -> None:
    screen.fill(SPACE_COLOR)

    half_map = map_half_extents(MAP_W, MAP_H)
    _draw_star_field(screen, camera, half_map, STAR_CELL_SPACING, STAR_DENSITY, salt=41)
    _draw_star_field(screen, camera, half_map, STAR_FINE_SPACING, STAR_FINE_DENSITY, salt=89)


def _draw_star_field(
    screen: pygame.Surface,
    camera: Camera,
    half_map: Vec2,
    step: float,
    density: float,
    salt: int,
) -> None:
    left, right, top, bottom = _visible_world_rect(camera)
    start_x = int((left - step) // step)
    end_x = int((right + step) // step) + 1
    start_y = int((top - step) // step)
    end_y = int((bottom + step) // step) + 1

    for ix in range(start_x, end_x):
        for iy in range(start_y, end_y):
            h = _hash2(ix, iy, salt=salt)
            if ((h & 0xFFFF) / 65535.0) > density:
                continue
            jx = ((h >> 8) & 0xFF) / 255.0 - 0.5
            jy = ((h >> 16) & 0xFF) / 255.0 - 0.5
            wx = (ix + 0.5 + jx * 0.85) * step
            wy = (iy + 0.5 + jy * 0.85) * step
            if -half_map.x <= wx <= half_map.x and -half_map.y <= wy <= half_map.y:
                continue
            p = world_to_screen(Vec2(wx, wy), camera, WINDOW_W, WINDOW_H)
            if not (0 <= p.x <= WINDOW_W and 0 <= p.y <= WINDOW_H):
                continue
            pygame.draw.circle(screen, (255, 255, 255), (int(p.x), int(p.y)), 1)


def _draw_grass(screen: pygame.Surface, camera: Camera) -> None:
    meadow_half = meadow_half_extents(MAP_W, MAP_H, MAP_BORDER_WIDTH)
    tile = _get_grass_tile()
    _blit_world_tiles(
        screen,
        camera,
        tile,
        -meadow_half.x,
        -meadow_half.y,
        meadow_half.x * 2,
        meadow_half.y * 2,
    )


def _draw_mud_border(screen: pygame.Surface, camera: Camera) -> None:
    map_half = map_half_extents(MAP_W, MAP_H)
    meadow_half = meadow_half_extents(MAP_W, MAP_H, MAP_BORDER_WIDTH)
    tile = _get_mud_tile()

    strips = (
        (-map_half.x, -map_half.y, map_half.x * 2, MAP_BORDER_WIDTH),
        (-map_half.x, map_half.y - MAP_BORDER_WIDTH, map_half.x * 2, MAP_BORDER_WIDTH),
        (-map_half.x, -meadow_half.y, MAP_BORDER_WIDTH, meadow_half.y * 2),
        (map_half.x - MAP_BORDER_WIDTH, -meadow_half.y, MAP_BORDER_WIDTH, meadow_half.y * 2),
    )

    for left, top, width, height in strips:
        _blit_world_tiles(screen, camera, tile, left, top, width, height)


def _blit_world_tiles(
    screen: pygame.Surface,
    camera: Camera,
    tile: pygame.Surface,
    world_left: float,
    world_top: float,
    world_width: float,
    world_height: float,
) -> None:
    tile_w, tile_h = tile.get_size()
    wx = world_left
    while wx < world_left + world_width - 0.5:
        wy = world_top
        while wy < world_top + world_height - 0.5:
            p0 = world_to_screen(Vec2(wx, wy), camera, WINDOW_W, WINDOW_H)
            p1 = world_to_screen(Vec2(wx + tile_w, wy + tile_h), camera, WINDOW_W, WINDOW_H)
            dest = pygame.Rect(
                int(min(p0.x, p1.x)),
                int(min(p0.y, p1.y)),
                max(1, int(abs(p1.x - p0.x))),
                max(1, int(abs(p1.y - p0.y))),
            )
            if dest.colliderect(pygame.Rect(0, 0, WINDOW_W, WINDOW_H)):
                scaled = tile if dest.size == tile.get_size() else pygame.transform.scale(tile, dest.size)
                screen.blit(scaled, dest)
            wy += tile_h
        wx += tile_w


def _draw_trees(screen: pygame.Surface, camera: Camera, meadow_half: Vec2) -> None:
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
            if not _point_in_meadow(x, y, meadow_half):
                continue

            scale_t = ((h >> 24) & 0xFF) / 255.0
            scale = TREE_SCALE_MIN + (TREE_SCALE_MAX - TREE_SCALE_MIN) * scale_t
            p = world_to_screen(Vec2(x, y), camera, WINDOW_W, WINDOW_H)
            trunk_w = int(18 * scale)
            trunk_h = int(42 * scale)
            canopy_r = int(34 * scale)

            trunk = pygame.Rect(int(p.x - trunk_w / 2), int(p.y - trunk_h), trunk_w, trunk_h)
            pygame.draw.rect(screen, TREE_TRUNK_COLOR, trunk, border_radius=max(2, int(4 * scale)))

            canopy_center = (int(p.x), int(p.y - trunk_h))
            pygame.draw.circle(screen, TREE_CANOPY_COLOR, canopy_center, canopy_r)
            pygame.draw.circle(screen, TREE_CANOPY_OUTLINE_COLOR, canopy_center, canopy_r, 2)
