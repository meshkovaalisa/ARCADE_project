import arcade
from crystal_platformer.constants import *


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        self.title = arcade.Text(
            "⏸ ПАУЗА",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40,
            color=(0, 200, 255),
            font_size=40,
            anchor_x="center",
            bold=True
        )

        controls = [
            "A/D или ←/→ — бег",
            "ПРОБЕЛ — прыжок",
            "W/S или ↑/↓ — лестницы",
            "ESC — продолжить"
        ]

        self.control_texts = []
        y_pos = SCREEN_HEIGHT // 2 - 10
        for i, line in enumerate(controls):
            text = arcade.Text(
                line,
                SCREEN_WIDTH // 2, y_pos - i * 25,
                color=arcade.color.WHITE,
                font_size=16,
                anchor_x="center"
            )
            self.control_texts.append(text)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_draw(self):
        self.clear()
        self.title.draw()
        for text in self.control_texts:
            text.draw()

        hint = arcade.Text(
            "Нажми ESC чтобы продолжить",
            SCREEN_WIDTH // 2, 30,
            color=arcade.color.GRAY,
            font_size=12,
            anchor_x="center"
        )
        hint.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)