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

