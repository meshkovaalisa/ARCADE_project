import arcade
from crystal_platformer.constants import *


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
        self.score = 0
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

        tile_map = arcade.load_tilemap(LEVEL_1, scaling=TILE_SCALING)
        self.walls = tile_map.sprite_lists["walls"]
        self.collision = tile_map.sprite_lists["collision"]
        self.coins = tile_map.sprite_lists.get("coins", arcade.SpriteList())

        self.world_camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
            walls=self.collision
        )
        self.world_width = int(tile_map.width * tile_map.tile_width * TILE_SCALING)
        self.world_height = int(tile_map.height * tile_map.tile_height * TILE_SCALING)
        self.score_text = arcade.Text(
            f"Счёт: {self.score}",
            20,
            SCREEN_HEIGHT - 30,
            color=arcade.color.WHITE,
            font_size=16,
            anchor_x="left"
        )

    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.walls.draw()
        self.coins.draw()
        self.player_list.draw()

        self.gui_camera.use()
        self.score_text.draw()

    def on_update(self, delta_time):
        dx = 0
        if self.left and not self.right:
            dx = -1
        elif self.right and not self.left:
            dx = 1
        self.player.change_x = dx * PLAYER_SPEED
        self.physics_engine.update()
        collected = arcade.check_for_collision_with_list(self.player, self.coins)
        for coin in collected:
            coin.remove_from_sprite_lists()
            self.score += 1

        self.gui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self._update_camera(delta_time)
        self._update_camera(delta_time)
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
        if key == arcade.key.SPACE and self.physics_engine.can_jump():
            self.physics_engine.jump(JUMP_STRENGTH)

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

    def _update_camera(self, delta_time):
        px, py = self.player.center_x, self.player.center_y
        cam_x, cam_y = self.world_camera.position
        dz_left = cam_x - DEAD_ZONE_W // 2
        dz_right = cam_x + DEAD_ZONE_W // 2
        dz_bottom = cam_y - DEAD_ZONE_H // 2
        dz_top = cam_y + DEAD_ZONE_H // 2

        target_x, target_y = cam_x, cam_y
        if px < dz_left:
            target_x = px + DEAD_ZONE_W // 2
        elif px > dz_right:
            target_x = px - DEAD_ZONE_W // 2
        if py < dz_bottom:
            target_y = py + DEAD_ZONE_H // 2
        elif py > dz_top:
            target_y = py - DEAD_ZONE_H // 2

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        target_x = max(half_w, min(self.world_width - half_w, target_x))
        target_y = max(half_h, min(self.world_height - half_h, target_y))

        self.world_camera.position = (
            cam_x + (target_x - cam_x) * CAMERA_LERP,
            cam_y + (target_y - cam_y) * CAMERA_LERP
        )
