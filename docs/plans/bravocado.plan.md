---
name: pygame-avocado-shooter
overview: Build a top-down 2D shooter in Python/Pygame with a camera-scrolling world where the player stays centered, auto-fires toward the mouse every 500ms, and enemies slowly home in from off-screen until all are defeated or the player dies.
todos:
  - id: venv-bootstrap
    content: Set up venv + pygame dependency, create runnable windowed loop at 1000×800.
    status: pending
  - id: camera-world-space
    content: Implement world/screen coordinate system and scrolling background grid.
    status: pending
  - id: player-avocado
    content: Add centered player movement and procedural avocado rendering + aim indicator.
    status: pending
  - id: auto-fire-bullets
    content: Add 500ms auto-fire toward mouse, bullet updates, and TTL culling.
    status: pending
  - id: enemy-wave
    content: Spawn N enemies off-screen and move them toward the player.
    status: pending
  - id: collisions-states
    content: Add bullet/enemy collisions, player contact damage + HP, win/lose screens + restart.
    status: pending
isProject: false
---

# Pygame Avocado Shooter (camera-scrolling)

## Goals & constraints
- Window: **1000×800**.
- Player remains **visually centered**; the **world/map scrolls** under a camera.
- Movement: **arrow keys**.
- Aim: **mouse cursor**.
- Shooting: **automatic**, **1 bullet / 500ms**, fired toward the mouse.
- Enemies: spawn **outside the visible screen**, move slowly toward player, top-down.
- Win: **all enemies eliminated**. Lose: **player HP = 0** (e.g., enemy contact damage).
- Use a **Python virtual environment**. **No Docker**.
- Visuals: **procedural shapes**; player looks like an **avocado**.

## Technical approach (core design)
### World vs screen coordinates (camera)
- Maintain all entities in **world coordinates** (float `Vector2`): `player.pos`, `enemy.pos`, `bullet.pos`.
- Camera center follows the player:
  - `camera.pos = player.pos` (world position that should map to the center of the screen)
  - Conversion:
    - `world_to_screen(p) = p - camera.pos + (WINDOW_W/2, WINDOW_H/2)`
    - `screen_to_world(s) = s + camera.pos - (WINDOW_W/2, WINDOW_H/2)`
- Player is drawn at `(WINDOW_W/2, WINDOW_H/2)`; enemies/bullets are drawn via `world_to_screen`.

### Input & movement
- Arrow keys produce a direction vector `(dx, dy)`; normalize to avoid faster diagonal movement.
- Player movement updates `player.pos += dir * speed * dt`.
- Because the camera follows the player, the **world appears to move** while the player stays centered.

### Aiming and shooting
- Mouse cursor is in **screen coords**; convert to a world-space aim point each frame:
  - `mouse_world = screen_to_world(pygame.mouse.get_pos())`
  - `aim_dir = (mouse_world - player.pos).normalize()` (handle zero length)
- Auto-fire timer:
  - Track `last_shot_ms`; if `now_ms - last_shot_ms >= 500`, spawn a bullet.
- Bullet spawns at `player.pos + aim_dir * muzzle_offset` and moves in world space:
  - `bullet.pos += bullet.vel * dt` where `bullet.vel = aim_dir * bullet_speed`.
- Bullet lifetime:
  - Either time-based TTL (e.g. 1.5–2.0s) or distance-based, plus cull if far outside camera view.

### Enemies
- Spawn `N` enemies at random positions in a ring **outside the current visible area**.
  - Use camera/player world position and window half-extents to compute an “off-screen rectangle,” then spawn beyond it.
- Movement each frame:
  - `to_player = player.pos - enemy.pos`.
  - `enemy.vel = to_player.normalize() * enemy_speed`.
  - Update with `dt`.
- Contact damage:
  - If enemy within radius of player, subtract HP using a cooldown (e.g. 200–400ms) so it isn’t instant death.

### Collisions
- Use simple **circle collisions** (fast, easy):
  - bullet vs enemy: if `distance <= (bullet_r + enemy_r)`, kill enemy and bullet, increment score.
  - enemy vs player: if `distance <= (enemy_r + player_r)`, apply damage.

### Rendering (procedural “avocado” player)
- Draw in screen space at center:
  - Outer body: dark-green ellipse.
  - Inner flesh: lighter-green ellipse inset.
  - Pit: brown circle offset slightly down.
  - Optional: small highlight.
- Indicate facing/aim direction:
  - Draw a small line/triangle “gun” pointing from center toward mouse direction.
- Enemies: simple circles with outline; bullets: small bright circles.
- Optional grid or textured background:
  - A repeating grid in world space helps show the map moving (draw grid lines using `world_to_screen` with step size).

### Game states
- `PLAYING`, `WIN`, `GAME_OVER`.
- On win/game over, display centered text and allow restart (`R`) or quit (`ESC`).

## Project layout
- `[README.md](README.md)`: setup/run instructions.
- `[requirements.txt](requirements.txt)`: pin `pygame`.
- `[main.py](main.py)`: entry point, game loop, state management.
- Optional modules if you want it cleaner from day 1:
  - `[game/settings.py](game/settings.py)`: constants.
  - `[game/entities.py](game/entities.py)`: Player, Enemy, Bullet dataclasses.
  - `[game/camera.py](game/camera.py)`: world/screen transforms.
  - `[game/spawn.py](game/spawn.py)`: enemy spawn helpers.
  - `[game/ui.py](game/ui.py)`: text rendering helpers.

## Step-by-step implementation plan
1. **Environment & bootstrap**
   - Create venv (`python -m venv .venv`), install pygame, create `requirements.txt`.
   - Minimal `main.py` that opens a 1000×800 window, fixed FPS cap, delta-time (`dt`).

2. **Core math utilities (camera transforms)**
   - Add `world_to_screen` / `screen_to_world` functions.
   - Verify: draw a world grid and move a “player position” in world space; confirm the grid scrolls while the player stays centered.

3. **Player movement & centered rendering**
   - Implement arrow-key movement in world space with normalized diagonals.
   - Draw avocado player at screen center; draw a gun/aim indicator toward the mouse.

4. **Auto-fire bullets toward mouse**
   - Implement shooting cooldown (500ms) using `pygame.time.get_ticks()`.
   - Spawn bullets with velocity in aim direction, update bullets, cull bullets (TTL).

5. **Enemy spawning off-screen**
   - Implement `spawn_enemies(N, player_pos)` to place enemies outside the visible screen bounds.
   - Render enemies with camera transform.

6. **Enemy steering + collision & damage**
   - Enemies home toward the player with a slow speed.
   - Implement bullet-enemy circle collision: remove both on hit.
   - Implement enemy-player contact damage with a damage cooldown; add HP bar.

7. **Win/lose states & restart**
   - Win when no enemies remain.
   - Lose when HP <= 0.
   - Add restart handling (reinitialize game state) and basic UI text.

8. **Polish (optional but recommended)**
   - Add screen shake on damage, enemy spawn indicator, or simple sound effects (optional).
   - Tuning constants (speeds, radii, HP, enemy count).

## Key parameters to tune (initial defaults)
- `PLAYER_SPEED`: ~300 px/s (world units).
- `BULLET_SPEED`: ~700 px/s.
- `FIRE_INTERVAL_MS`: 500.
- `ENEMY_SPEED`: ~80–120 px/s.
- `ENEMY_COUNT`: e.g. 15–30.
- `PLAYER_HP`: e.g. 100; `CONTACT_DAMAGE`: e.g. 10 every 300ms.

## Minimal test plan
- Player remains centered while moving; background grid scrolls.
- Bullets travel toward mouse cursor consistently (including when moving).
- Enemies spawn off-screen and approach player.
- Bullet-enemy collisions remove enemies; win triggers when last enemy dies.
- Player HP decreases only on contact and triggers game over at 0.
