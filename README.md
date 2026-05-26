# Pygame Avocado Shooter

Top-down 2D shooter built with Python and Pygame. You play as Bravocado in a scrolling meadow, auto-fire at enemies, and survive until every enemy is defeated—or until your HP runs out.

## Main functionalities

### Camera and world space
- The player stays **visually centered** on screen; the world scrolls around you.
- Entities (enemies, bullets, background) live in **world coordinates** and are drawn via `world_to_screen` transforms in `game/camera.py`.
- Movement and simulation use **delta time** (`dt`) so speed stays consistent across frame rates.

### Player movement and aiming
- Move with **arrow keys** or **WASD** (diagonal movement is normalized).
- Aim with the **mouse**; a custom crosshair replaces the system cursor during play.
- The hero sprite (`img/bravocado-points-one-hand-no-bg.PNG`) faces left or right based on aim direction.

### Auto-fire combat
- Bullets fire **automatically** toward the mouse at a configurable interval (`FIRE_INTERVAL_MS` in `game/settings.py`).
- Bullets spawn slightly ahead of the player, travel in world space, and despawn after a time-to-live (`BULLET_TTL_MS`).
- **Circle collisions** between bullets and enemies remove both on hit.

### Enemies
- Enemies spawn in a ring **outside the visible screen** and **home toward the player** each frame.
- Enemies are drawn as procedural red circles with an angry face (eyes, brows, mouth).
- Enemy count, speed, spawn distance, and radius are tunable in `game/settings.py`.

### Health and contact damage
- The player has an **HP bar** (top-left) with color feedback (green → yellow → red).
- Touching an enemy applies **contact damage** on a cooldown (`CONTACT_DAMAGE_COOLDOWN_MS`), not instant death.
- On damage, a short **screen shake** gives visual feedback (`SCREEN_SHAKE_*` settings).

### Win, lose, and restart
- **Win:** defeat all enemies.
- **Lose:** HP reaches 0.
- End screens show overlay text; press **R** to restart the round or **ESC** to quit.

### Procedural meadow background
- Each run generates a **random dusk-green meadow** (seeded layout): grass patches, muted flowers, and scattered trees.
- Background and trees are **visual only**—they do not block movement or affect collisions.
- Tree density, scale, and meadow colors are configured in `game/settings.py`.

## Controls

| Action | Keys |
|--------|------|
| Move | Arrow keys or WASD |
| Aim | Mouse |
| Restart (after win/lose) | R |
| Quit | ESC or close window |

## Project layout

| Path | Role |
|------|------|
| `main.py` | Game loop, input, entities, collisions, rendering, game states |
| `game/settings.py` | Tunable constants (speeds, HP, enemies, meadow, shake) |
| `game/camera.py` | Camera dataclass and world ↔ screen transforms |
| `game/background.py` | Procedural meadow and tree drawing |
| `img/` | Hero sprite assets |

## Configuration

Gameplay feel is controlled in `game/settings.py`. Useful knobs include:

- `PLAYER_SPEED`, `PLAYER_HP_MAX`, `PLAYER_RADIUS`
- `FIRE_INTERVAL_MS`, `BULLET_SPEED`, `BULLET_TTL_MS`
- `ENEMY_COUNT`, `ENEMY_SPEED`, `ENEMY_SPAWN_PADDING`, `ENEMY_SPAWN_EXTRA`
- `CONTACT_DAMAGE`, `CONTACT_DAMAGE_COOLDOWN_MS`
- `SCREEN_SHAKE_DURATION_MS`, `SCREEN_SHAKE_AMPLITUDE`
- Meadow/tree colors and `TREE_DENSITY`

## Setup (Windows / PowerShell)

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the game:

```powershell
python main.py
```
