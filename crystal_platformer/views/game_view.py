import arcade
from crystal_platformer.constants import *
from views.pause_view import PauseView
from views.level_complete_view import LevelCompleteView
from arcade.particles import Emitter, EmitBurst, FadeParticle


class GameView(arcade.View):
    def __init__(self, level=1):
        super().__init__()
        self.setup(level)

    def setup(self, level=1):
        self.current_level = level
        self.idle_texture = arcade.load_texture(f"{TEXTURE_PATH_PREFIX}{TEXTURE_FILE_PREFIX}idle.png")
        self.player = arcade.Sprite()
        self.player.texture = self.idle_texture
        self.player.scale = PLAYER_SCALE
        self.player_speed = PLAYER_SPEED
        self.is_dead = False
        self.has_shield = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.has_key = False
        self.door_open = False
        self.score = 0
        self.walk_textures = []
        for i in range(WALK_FRAMES_COUNT):
            texture = arcade.load_texture(f"{TEXTURE_PATH_PREFIX}{TEXTURE_FILE_PREFIX}walk{i}.png")
            self.walk_textures.append(texture)
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = TEXTURE_CHANGE_DELAY
        self.climb_textures = []
        for i in range(CLIMB_FRAMES_COUNT):
            tex = arcade.load_texture(f"{TEXTURE_PATH_PREFIX}{TEXTURE_FILE_PREFIX}climb{i}.png")
            self.climb_textures.append(tex)

        if level == 1:
            self.player.center_x = SCREEN_WIDTH // 2
            self.player.center_y = SCREEN_HEIGHT // 2
        elif level == 2:
            self.player.center_x = 70
            self.player.center_y = 1390

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        level_path = LEVEL_1 if level == 1 else LEVEL_2
        tile_map = arcade.load_tilemap(level_path, scaling=TILE_SCALING)
        self.walls = tile_map.sprite_lists["walls"]
        self.collision = tile_map.sprite_lists["collision"]
        self.coins = tile_map.sprite_lists.get("coins", arcade.SpriteList())
        self.ladders = tile_map.sprite_lists.get("ladders", arcade.SpriteList())
        self.traps = tile_map.sprite_lists.get("traps", arcade.SpriteList())
        self.shooters = tile_map.sprite_lists.get("shooters", arcade.SpriteList())
        self.shields = tile_map.sprite_lists.get("shields", arcade.SpriteList())
        self.shield_texture = arcade.load_texture(SHIELD_TEXTURE)
        self.key = tile_map.sprite_lists.get("key", arcade.SpriteList())
        self.door = tile_map.sprite_lists.get("door", arcade.SpriteList())

        self.collision.append(self.door[0])

        key_path = KEY_TEXTURE if level == 1 else KEY_TEXTURE_2
        self.key_texture = arcade.load_texture(key_path)

        self.portal = tile_map.sprite_lists.get("portal", arcade.SpriteList())

        self.moving_platforms = arcade.SpriteList()
        self.platform_trains = []

        raw_tiles = tile_map.sprite_lists.get("moving_platforms", [])

        if raw_tiles:
            raw_tiles.sort(key=lambda t: t.center_y)

            current_row = []
            for tile in raw_tiles:
                if current_row and abs(tile.center_y - current_row[0].center_y) > 10:
                    self._process_row(current_row)
                    current_row = []
                current_row.append(tile)
            if current_row:
                self._process_row(current_row)

            for train in self.platform_trains:
                for tile in train:
                    if tile not in self.moving_platforms:
                        self.moving_platforms.append(tile)

        self.projectiles = arcade.SpriteList()
        self.shoot_timer = 0
        self.shoot_interval = SHOOT_INTERVAL

        self.world_camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
            walls=self.collision
        )
        self.on_ladder = False
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
        self.pause_hint = arcade.Text(
            "ESC — пауза",
            SCREEN_WIDTH - 20,
            20,
            color=NEON_BLUE,
            font_size=12,
            anchor_x="right"
        )

        self.lives = MAX_LIVES
        self.is_invulnerable = False
        self.inv_timer = 0
        self.lives_text = arcade.Text(
            f"❤️ {self.lives}",
            SCREEN_WIDTH - 70,
            SCREEN_HEIGHT - 30,
            color=arcade.color.RED,
            font_size=20,
            anchor_x="left"
        )

        self.shield_text = arcade.Text(
            "🛡️",
            SCREEN_WIDTH - 120,
            SCREEN_HEIGHT - 30,
            color=arcade.color.CYAN,
            font_size=20,
            anchor_x="left"
        )
        self.shield_text.visible = False

        self.jump_sound = arcade.load_sound(JUMP_SOUND)
        self.coin_sound = arcade.load_sound(COIN_SOUND)
        self.death_sound = arcade.load_sound(DEATH_SOUND)
        self.emitters = []
        self.projectile_texture = arcade.load_texture(SAW_TEXTURE)

    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.walls.draw()
        self.ladders.draw()
        self.traps.draw()
        self.moving_platforms.draw()
        self.shooters.draw()
        self.coins.draw()
        self.projectiles.draw()
        self.player_list.draw()
        self.shields.draw()
        self.door.draw()
        self.key.draw()
        self.portal.draw()
        for emitter in self.emitters:
            emitter.draw()

        self.gui_camera.use()
        self.score_text.draw()
        self.lives_text.draw()
        self.pause_hint.draw()
        self.shield_text.visible = self.has_shield
        if self.has_shield:
            self.shield_text.draw()
        if self.has_key:
            arcade.draw_texture_rect(self.key_texture, arcade.XYWH(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 30, 40, 40))

    def on_update(self, delta_time):
        if self.is_invulnerable:
            self.inv_timer -= delta_time
            self.player.alpha = 100 if int(self.inv_timer * 10) % 2 == 0 else 255
            if self.inv_timer <= 0:
                self.is_invulnerable = False
                self.player.alpha = 255
        if self.is_dead:
            for emitter in self.emitters:
                emitter.update(delta_time)
            if all(e.can_reap() for e in self.emitters):
                self.setup(self.current_level)
            return

        if self.on_ladder and (self.left or self.right):
            self.on_ladder = False
            self.player.center_x += LADDER_SPEED if self.right else -LADDER_SPEED

        touching_ladders = arcade.check_for_collision_with_list(self.player, self.ladders)

        if touching_ladders and not (self.left or self.right):
            self.on_ladder = True
        else:
            self.on_ladder = False
        if self.on_ladder:
            self.physics_engine.gravity_constant = 0
            if self.up:
                self.player.change_y = LADDER_SPEED
            elif self.down:
                self.player.change_y = -LADDER_SPEED
            else:
                self.player.change_y = 0
            if touching_ladders and not (self.left or self.right):
                nearest = min(touching_ladders, key=lambda l: abs(l.center_x - self.player.center_x))
                self.player.center_x += (nearest.center_x - self.player.center_x) * 0.2
        else:
            self.physics_engine.gravity_constant = GRAVITY

        if self.left:
            self.player.change_x = -PLAYER_SPEED
        elif self.right:
            self.player.change_x = PLAYER_SPEED
        else:
            self.player.change_x = 0

        self.physics_engine.update()

        for train in self.platform_trains:
            leader = train[0]

            check_x = train[-1].right + 3 if leader.direction > 0 else train[0].left - 3
            if arcade.get_sprites_at_point((check_x, leader.center_y), self.collision):
                leader.direction *= -1
            else:
                leader.center_x += leader.speed * leader.direction
                if abs(leader.center_x - leader.start_x) > leader.distance:
                    leader.direction *= -1

            for i, tile in enumerate(train):
                tile.center_x = leader.center_x + leader.offsets[i]

            if (self.player.bottom <= train[0].top + 12 and
                    self.player.bottom >= train[0].top - 5 and
                    self.player.center_x > train[0].left and
                    self.player.center_x < train[-1].right and
                    self.player.change_y <= 0):
                self.player.bottom = train[0].top
                self.player.change_y = 0
                self.player.center_x += leader.speed * leader.direction

        self.shoot_timer += delta_time
        if self.shoot_timer >= self.shoot_interval and len(self.shooters) > 0:
            self.fire_projectiles()
            self.shoot_timer = 0
        if arcade.check_for_collision_with_list(self.player, self.traps):
            self.take_damage()
            return

        for proj in self.projectiles[:]:
            proj.center_x += proj.change_x * delta_time
            proj.center_y += proj.change_y * delta_time

            if arcade.check_for_collision(self.player, proj):
                self.take_damage()
                proj.remove_from_sprite_lists()
                continue

            if (proj.center_x < -200 or proj.center_x > self.world_width + 200 or
                    proj.center_y < -200 or proj.center_y > self.world_height + 200):
                proj.remove_from_sprite_lists()

        collected = arcade.check_for_collision_with_list(self.player, self.coins)
        for coin in collected:
            coin.remove_from_sprite_lists()
            self.score += 1
            self.score_text.text = f"Счёт: {self.score}"
            arcade.play_sound(self.coin_sound)
            self.create_coin_effect(coin.center_x, coin.center_y)
        if not self.has_shield:
            collected_shields = arcade.check_for_collision_with_list(self.player, self.shields)
            for shield in collected_shields:
                shield.remove_from_sprite_lists()
                self.has_shield = True

        if not self.has_key and len(self.key) > 0:
            if arcade.check_for_collision_with_list(self.player, self.key):
                self.key[0].remove_from_sprite_lists()
                self.has_key = True

        if self.score >= 5 and not self.door_open and len(self.door) > 0:
            self.door_open = True
            door_tile = self.door[0]
            if door_tile in self.collision:
                self.collision.remove(door_tile)
            door_tile.remove_from_sprite_lists()

        self.gui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self._update_camera(delta_time)
        self.update_animation(delta_time)

        for emitter in self.emitters:
            emitter.update(delta_time)
        self.emitters = [e for e in self.emitters if not e.can_reap()]
        if arcade.check_for_collision_with_list(self.player, self.portal):
            if self.has_key:
                self.window.show_view(LevelCompleteView(level=self.current_level, score=self.score))
                return

    def on_key_press(self, key, modifiers):
        if self.is_dead: return
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        if key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
        if key in (arcade.key.UP, arcade.key.W):
            self.up = True
        if key in (arcade.key.DOWN, arcade.key.S):
            self.down = True
        if key == arcade.key.SPACE and not self.on_ladder:
            on_ground = self.physics_engine.can_jump()
            on_platform = self.is_on_moving_platform()

            if on_ground or on_platform:
                self.player.change_y = JUMP_STRENGTH
                arcade.play_sound(self.jump_sound)
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))

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
        if self.on_ladder and (self.up or self.down) and len(self.climb_textures) > 0:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.climb_textures):
                    self.current_texture = 0
                self.player.texture = self.climb_textures[self.current_texture]
            return
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

    def create_coin_effect(self, x, y):
        if len(self.emitters) > 10:
            return
        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitBurst(15),
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(4, arcade.color.YELLOW),
                change_xy=arcade.math.rand_in_circle((0.0, 0.0), 4.0),
                lifetime=0.5,
                start_alpha=255,
                end_alpha=0
            )
        )
        self.emitters.append(emitter)

    def restart_game(self):
        self.setup()

    def create_death_effect(self, x, y):
        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitBurst(50),
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(6, arcade.color.RED),
                change_xy=arcade.math.rand_in_circle((0.0, 0.0), 6.0),
                lifetime=1.5,
                start_alpha=255,
                end_alpha=0
            )
        )
        self.emitters.append(emitter)

    def die(self):
        self.is_dead = True
        self.player.visible = False
        self.create_death_effect(self.player.center_x, self.player.center_y)
        arcade.play_sound(self.death_sound)

    def fire_projectiles(self):
        for shooter in self.shooters:
            proj = arcade.Sprite()
            proj.texture = self.projectile_texture
            proj.center_x = shooter.center_x
            proj.center_y = shooter.center_y
            proj.scale = SAW_SCALE

            dx = self.player.center_x - proj.center_x
            dy = self.player.center_y - proj.center_y
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)

            proj.change_x = (dx / distance) * 30
            proj.change_y = (dy / distance) * 30

            self.projectiles.append(proj)

    def create_shoot_effect(self, x, y):
        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitBurst(8),
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(3, arcade.color.ORANGE),
                change_xy=arcade.math.rand_in_circle((0.0, 0.0), 2.0),
                lifetime=0.3,
                start_alpha=255,
                end_alpha=0
            )
        )
        self.emitters.append(emitter)

    def take_damage(self):
        if self.is_invulnerable:
            return
        if self.has_shield:
            self.has_shield = False
            self.is_invulnerable = True
            self.inv_timer = 0.5
            return
        self.lives -= 1
        self.lives_text.text = f"❤️ {self.lives}"
        self.is_invulnerable = True
        self.inv_timer = INVULNERABILITY_TIME
        self.player.center_y += 10
        if self.lives <= 0:
            self.die()

    def reset_player(self):
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.change_x = 0
        self.player.change_y = 0
        self.is_dead = False
        self.is_invulnerable = False
        self.player.visible = True
        self.player.alpha = 255

    def _process_row(self, row_tiles):
        row_tiles.sort(key=lambda t: t.center_x)

        current_train = [row_tiles[0]]
        for i in range(1, len(row_tiles)):
            prev_tile = current_train[-1]
            curr_tile = row_tiles[i]

            if abs(curr_tile.left - prev_tile.right) < 5:
                current_train.append(curr_tile)
            else:
                self._setup_train(current_train)
                current_train = [curr_tile]
        self._setup_train(current_train)

    def _setup_train(self, train):
        leader = train[0]
        leader.start_x = leader.center_x
        leader.speed = 2
        leader.direction = 1
        leader.distance = 150
        leader.offsets = [tile.center_x - leader.center_x for tile in train]
        self.platform_trains.append(train)

    def is_on_moving_platform(self):
        for train in self.platform_trains:
            if (self.player.center_x > train[0].left and
                    self.player.center_x < train[-1].right and
                    abs(self.player.bottom - train[0].top) < 20):
                return True
        return False
