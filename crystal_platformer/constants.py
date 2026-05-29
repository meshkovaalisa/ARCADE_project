import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Crystal Platformer"
BG_COLOR = arcade.color.DARK_SLATE_GRAY

MENU_TITLE_SIZE = 40
MENU_HINT_SIZE = 20
TEXT_COLOR = arcade.color.WHITE

FPS = 60

PLAYER_SPEED = 5
PLAYER_SCALE = 0.3
TEXTURE_PATH_PREFIX = ":resources:/images/animated_characters/male_person/"
TEXTURE_FILE_PREFIX = "malePerson_"
WALK_FRAMES_COUNT = 8
TEXTURE_CHANGE_DELAY = 0.1

LEVEL_1 = "maps/level1.tmx"
LEVEL_2 = "maps/level2.tmx"
TILE_SCALING = 0.5
MOVING_PLATFORM_SCALE = 0.6

LADDER_SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = 8

CAMERA_LERP = 0.12
DEAD_ZONE_W = 200
DEAD_ZONE_H = 150

JUMP_SOUND = ":resources:/sounds/jump1.wav"
COIN_SOUND = ":resources:/sounds/coin1.wav"
DEATH_SOUND = ":resources:/sounds/hurt1.wav"

SHIELD_TEXTURE = "assets/shield.png"
KEY_TEXTURE = "assets/key.png"
KEY_TEXTURE_2 = "assets/key_green.png"
SAW_TEXTURE = "assets/saw.png"

SAW_SCALE = 0.05

MAX_LIVES = 3
INVULNERABILITY_TIME = 2.0
CLIMB_FRAMES_COUNT = 3
SHOOT_INTERVAL = 4.0

NEON_BLUE = (0, 200, 255)
NEON_GREEN = (0, 255, 150)
NEON_PINK = (255, 50, 150)


