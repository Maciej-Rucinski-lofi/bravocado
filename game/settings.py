WINDOW_W, WINDOW_H = 1000, 800
FPS_CAP = 120

BG_COLOR = (18, 18, 22)

GRID_SPACING = 80  # world units (pixels)
GRID_MINOR_COLOR = (38, 38, 46)
GRID_MAJOR_COLOR = (60, 60, 75)
GRID_MAJOR_EVERY = 5  # major line every N minor lines

# Meadow background (visual-only, no collisions)
MEADOW_BASE_COLOR = (78, 168, 88)
MEADOW_PATCH_COLOR = (92, 186, 98)
MEADOW_PATCH_SPACING = 260.0
MEADOW_PATCH_RADIUS = 150.0
MEADOW_FLOWER_DENSITY = 0.8
MEADOW_FLOWER_COLORS = (
    (250, 245, 235),  # white
    (255, 232, 120),  # yellow
    (255, 168, 198),  # pink
    (190, 210, 255),  # light blue
)

TREE_TRUNK_COLOR = (105, 72, 40)
TREE_CANOPY_COLOR = (42, 120, 58)
TREE_CANOPY_OUTLINE_COLOR = (22, 70, 36)

# Each entry: (x_world, y_world, scale)
TREE_SPECS = (
    (-420.0, -260.0, 1.05),
    (380.0, -320.0, 1.15),
    (760.0, 140.0, 0.95),
    (-780.0, 220.0, 1.25),
    (120.0, 520.0, 1.10),
    (-160.0, 820.0, 0.90),
)

PLAYER_SPEED = 320.0  # world units per second

# Player hero sprite (screen-space, centered)
PLAYER_SPRITE_PATH = "img/bravocado-points-one-hand-no-bg.PNG"
PLAYER_SPRITE_SIZE = (110, 110)

# Step 4: auto-fire bullets
FIRE_INTERVAL_MS = 500
BULLET_SPEED = 700.0
BULLET_TTL_MS = 1800
BULLET_RADIUS = 5
BULLET_MUZZLE_OFFSET = 52.0
BULLET_COLOR = (255, 220, 90)

# Step 5: enemy spawn + rendering
ENEMY_COUNT = 18
ENEMY_RADIUS = 20
ENEMY_SPAWN_PADDING = 140.0
ENEMY_SPAWN_EXTRA = 260.0
ENEMY_BODY_COLOR = (190, 55, 55)
ENEMY_OUTLINE_COLOR = (45, 12, 12)
ENEMY_FACE_COLOR = (28, 8, 8)
ENEMY_SPEED = 96.0

# Step 6: contact damage + HP
PLAYER_RADIUS = 28
PLAYER_HP_MAX = 100
CONTACT_DAMAGE = 10
CONTACT_DAMAGE_COOLDOWN_MS = 300
HP_BAR_W = 220
HP_BAR_H = 18
HP_BAR_MARGIN = 16
