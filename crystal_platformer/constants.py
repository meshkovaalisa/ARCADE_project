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
TILE_SCALING = 0.5

LADDER_SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = 16

CAMERA_LERP = 0.12
DEAD_ZONE_W = 200
DEAD_ZONE_H = 150

JUMP_SOUND = ":resources:/sounds/jump1.wav"
COIN_SOUND = ":resources:/sounds/coin1.wav"
