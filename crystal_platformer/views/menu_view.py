import arcade
import math
import random
from crystal_platformer.constants import *
from views.game_view import GameView


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.title = arcade.Text(
            "CRYSTAL\nPLATFORMER",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80,
            color=NEON_BLUE,
            font_size=42,
            anchor_x="center",
            bold=True
        )

        self.start_text = arcade.Text(
            "▶ НАЖМИ ПРОБЕЛ ДЛЯ СТАРТА",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center"
        )

        self.instructions = [
            "УПРАВЛЕНИЕ:",
            "A / D или ← / →  —  Бег",
            "ПРОБЕЛ  —  Прыжок",
            "W / S или ↑ / ↓  —  Лестницы",
            "ESC  —  Пауза",
            "",
            "ЦЕЛЬ:",
            "Собери все монеты",
            "Избегай лавы и пил",
            "Найди ключ и после найди портал для победы!",
            "",
            "❤️ У тебя 3 жизни — береги их!"
        ]

        self.instruction_texts = []
        y_pos = 170
        for line in self.instructions:
            if line.strip() == "":
                y_pos -= 8
                continue
            color = NEON_GREEN if "УПРАВЛЕНИЕ" in line or "ЦЕЛЬ" in line or "❤️" in line else arcade.color.WHITE
            size = 14 if "УПРАВЛЕНИЕ" in line or "ЦЕЛЬ" in line else 12

            text = arcade.Text(
                line,
                SCREEN_WIDTH / 2, y_pos,
                color=color,
                font_size=size,
                anchor_x="center"
            )
            self.instruction_texts.append(text)
            y_pos -= 13

        self.pulse = 0
        self.particles = []
        for _ in range(40):
            self.particles.append({
                'x': random.uniform(0, SCREEN_WIDTH),
                'y': random.uniform(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2.5),
                'size': random.randint(2, 5),
                'alpha': random.randint(50, 150)
            })

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_update(self, delta_time):
        self.pulse += delta_time * 2

        alpha = int(180 + 75 * math.sin(self.pulse))
        self.start_text.color = (255, 255, 255, alpha)

        for p in self.particles:
            p['y'] += p['speed']
            if p['y'] > SCREEN_HEIGHT + 10:
                p['y'] = -10
                p['x'] = random.uniform(0, SCREEN_WIDTH)

    def on_draw(self):
        self.clear()

        for p in self.particles:
            arcade.draw_circle_filled(p['x'], p['y'], p['size'], (*NEON_BLUE, p['alpha']))

        self.title.draw()
        for text in self.instruction_texts:
            text.draw()
        self.start_text.draw()

        hint = arcade.Text(
            "Нажми ESC для паузы",
            SCREEN_WIDTH / 2, 25,
            color=arcade.color.GRAY,
            font_size=12,
            anchor_x="center"
        )
        hint.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game = GameView()
            game.setup()
            self.window.show_view(game)
