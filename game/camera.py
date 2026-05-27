from __future__ import annotations

from dataclasses import dataclass

import pygame


Vec2 = pygame.math.Vector2


@dataclass
class Camera:
    pos: Vec2


def world_to_screen(world_pos: Vec2, camera: Camera, window_w: int, window_h: int) -> Vec2:
    return world_pos - camera.pos + Vec2(window_w / 2, window_h / 2)


def screen_to_world(screen_pos: Vec2, camera: Camera, window_w: int, window_h: int) -> Vec2:
    return screen_pos + camera.pos - Vec2(window_w / 2, window_h / 2)


def map_half_extents(map_w: int, map_h: int) -> Vec2:
    return Vec2(map_w / 2, map_h / 2)


def meadow_half_extents(map_w: int, map_h: int, border_width: float) -> Vec2:
    return map_half_extents(map_w, map_h) - Vec2(border_width, border_width)


def playable_half_extents(
    map_w: int,
    map_h: int,
    border_width: float,
    edge_margin: float,
) -> Vec2:
    return meadow_half_extents(map_w, map_h, border_width) - Vec2(edge_margin, edge_margin)


def clamp_pos_to_map_island(
    pos: Vec2,
    map_w: int,
    map_h: int,
    radius: float = 0.0,
) -> Vec2:
    """Keep a circular entity inside the map island (meadow + mud), out of outer space."""
    half_map = map_half_extents(map_w, map_h)
    return Vec2(
        max(-half_map.x + radius, min(half_map.x - radius, pos.x)),
        max(-half_map.y + radius, min(half_map.y - radius, pos.y)),
    )


def clamp_player_centered(
    player_pos: Vec2,
    window_w: int,
    window_h: int,
    map_w: int,
    map_h: int,
    border_width: float,
    edge_margin: float,
) -> Vec2:
    """Hero centered on camera; stays in meadow, never enters the mud ring."""
    playable_half = playable_half_extents(map_w, map_h, border_width, edge_margin)

    return Vec2(
        max(-playable_half.x, min(playable_half.x, player_pos.x)),
        max(-playable_half.y, min(playable_half.y, player_pos.y)),
    )
