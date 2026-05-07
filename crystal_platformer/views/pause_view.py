import arcade
from pyglet.graphics import Batch
from crystal_platformer.constants import BG_COLOR, TEXT_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.batch = Batch()

        self.pause_text = arcade.Text(
            "ПАУЗА",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
            TEXT_COLOR, font_size=40, anchor_x="center", batch=self.batch
        )
        self.hint_text = arcade.Text(
            "Нажми ESC, чтобы продолжить",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20,
            TEXT_COLOR, font_size=20, anchor_x="center", batch=self.batch
        )

    def on_show_view(self):
        arcade.set_background_color(BG_COLOR)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)