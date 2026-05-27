WINDOW_W, WINDOW_H = 1000, 800
FPS_CAP = 120

# World island (centered on origin): meadow inside, mud ring, space beyond.
MAP_W = WINDOW_W * 3
MAP_H = WINDOW_H * 3
# Space outside the map (visible when camera nears edges)
SPACE_COLOR = (0, 0, 0)
STAR_CELL_SPACING = 100.0
STAR_DENSITY = 0.78
STAR_FINE_SPACING = 52.0
STAR_FINE_DENSITY = 0.62

BG_COLOR = (18, 18, 22)

GRID_SPACING = 80  # world units (pixels)
GRID_MINOR_COLOR = (38, 38, 46)
GRID_MAJOR_COLOR = (60, 60, 75)
GRID_MAJOR_EVERY = 5  # major line every N minor lines

# Meadow grass background (tiled sprite, visual-only)
GRASS_SPRITE_PATH = "img/background/grass.png"

TREE_TRUNK_COLOR = (105, 72, 40)
TREE_CANOPY_COLOR = (28, 84, 50)
TREE_CANOPY_OUTLINE_COLOR = (16, 48, 30)
TREE_CELL_SPACING = 260.0
TREE_DENSITY = 0.42  # chance [0..1] for a tree in each cell
TREE_SCALE_MIN = 0.85
TREE_SCALE_MAX = 1.30

PLAYER_SPEED = 320.0  # world units per second

# Player hero sprite (screen-space, centered)
PLAYER_SPRITE_PATH = "img/bravocado-points-one-hand-no-bg.PNG"
PLAYER_SPRITE_SIZE = (110, 110)

# Mud border ring (same width as hero sprite)
MUD_BORDER_SPRITE_PATH = "img/background/mud.jpg"
MAP_BORDER_WIDTH = PLAYER_SPRITE_SIZE[0]
# Keep hero body inside the meadow (clear of the mud ring)
PLAYABLE_EDGE_MARGIN = PLAYER_SPRITE_SIZE[0] * 0.5 + 12.0

# Step 4: auto-fire bullets
# FIRE_INTERVAL_MS = 200
FIRE_INTERVAL_MS = 20 # Just for testing
BULLET_SPEED = 700.0
BULLET_TTL_MS = 1800
BULLET_RADIUS = 5
BULLET_MUZZLE_OFFSET = 52.0
BULLET_COLOR = (255, 220, 90)
TRIPLE_SHOT_SPREAD_DEG = 14.0  # total angle between outer bullets

# Step 5: enemy spawn + rendering
ENEMY_COUNT = 200
ENEMY_RADIUS = 20
ENEMY_SPAWN_PADDING = 100.0
ENEMY_SPAWN_EXTRA = 260.0
# When the hero is this close to a playable edge, enemies won't enter from that side.
ENEMY_SPAWN_BORDER_BUFFER = 280.0
ENEMY_BODY_COLOR = (190, 55, 55)
ENEMY_OUTLINE_COLOR = (45, 12, 12)
ENEMY_FACE_COLOR = (28, 8, 8)
ENEMY_SPEED = 110.0
# Spawn pacing: slow at round start, faster as more enemies enter the queue
ENEMY_SPAWN_INTERVAL_START_MS = 700
ENEMY_SPAWN_INTERVAL_END_MS = 90
ENEMY_SPAWN_RAMP_POWER = 10.0  # higher = sharper ramp (try 2–4 normal, 6–12 intense)

# Step 6: contact damage + HP
PLAYER_RADIUS = 28
PLAYER_HP_MAX = 100
# CONTACT_DAMAGE = 10
CONTACT_DAMAGE = 0 # for testing
CONTACT_DAMAGE_COOLDOWN_MS = 300
SCREEN_SHAKE_DURATION_MS = 180
SCREEN_SHAKE_AMPLITUDE = 10.0
HP_BAR_W = 300
HP_BAR_H = 18
HP_BAR_MARGIN = 16

SCORE_PER_KILL = 10
