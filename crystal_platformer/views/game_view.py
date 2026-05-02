import arcade
from crystal_platformer.constants import PLAYER_SPEED, TEXTURE_PATH_PREFIX, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SCALE, \
    WALK_FRAMES_COUNT, TEXTURE_CHANGE_DELAY, TEXTURE_FILE_PREFIX


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.idle_texture = arcade.load_texture(f"{TEXTURE_PATH_PREFIX}{TEXTURE_FILE_PREFIX}idle.png")
        self.player = arcade.Sprite()
        self.player.texture = self.idle_texture
        self.player.scale = PLAYER_SCALE
        self.player_speed = PLAYER_SPEED
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walk_textures = []
        for i in range(WALK_FRAMES_COUNT):
            texture = arcade.load_texture(f"{TEXTURE_PATH_PREFIX}{TEXTURE_FILE_PREFIX}walk{i}.png")
            self.walk_textures.append(texture)
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = TEXTURE_CHANGE_DELAY

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        dx = 0
        if self.left: dx -= self.player_speed
        if self.right: dx += self.player_speed
        self.player.center_x += dx * delta_time
        half_w = self.player.width / 2
        self.player.center_x = max(half_w, min(SCREEN_WIDTH - half_w, self.player.center_x))
        self.update_animation(delta_time)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        if key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
        if key in (arcade.key.UP, arcade.key.W):
            self.up = True
        if key in (arcade.key.DOWN, arcade.key.S):
            self.down = True

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
        if key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
        if key in (arcade.key.UP, arcade.key.W):
            self.up = False
        if key in (arcade.key.DOWN, arcade.key.S):
            self.down = False

    def update_animation(self, delta_time):
        if self.left or self.right:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                base_tex = self.walk_textures[self.current_texture]
                if self.left and not self.right:
                    self.player.texture = base_tex.flip_horizontally()
                else:
                    self.player.texture = base_tex
        else:
            self.player.texture = (
                self.idle_texture.flip_horizontally()
                if (self.left and not self.right)
                else self.idle_texture
            )
            self.current_texture = 0