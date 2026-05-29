import arcade
import os
from crystal_platformer.constants import *


class LevelCompleteView(arcade.View):
    def __init__(self, level, score):
        super().__init__()
        self.level = level
        self.score = score
        self.nickname = ""
        self.typing = True
        self.scores = self.load_scores()
        self.is_last_level = (self.level == 2)

        self.title = arcade.Text(
            "Уровень пройден!",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100,
            arcade.color.GOLD, 32,
            anchor_x="center", bold=True
        )
        self.score_label = arcade.Text(
            f"Счёт: {self.score}",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 160,
            arcade.color.WHITE, 24,
            anchor_x="center"
        )
        self.input_prompt = arcade.Text(
            "Введите имя и нажмите Enter:",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
            arcade.color.CYAN, 20,
            anchor_x="center"
        )
        self.nickname_text = arcade.Text(
            "",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            arcade.color.WHITE, 28,
            anchor_x="center"
        )
        self.leaderboard_title = arcade.Text(
            "Топ-3:",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80,
            arcade.color.GOLD, 22,
            anchor_x="center", bold=True
        )
        if self.is_last_level:
            self.next_hint = arcade.Text(
                "Вы прошли игру!",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120,
                arcade.color.GOLD, 20,
                anchor_x="center", bold=True
            )
        else:
            self.next_hint = arcade.Text(
                "ENTER — следующий уровень",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120,
                arcade.color.GREEN, 18,
                anchor_x="center"
            )

        self.menu_hint = arcade.Text(
            "ESC — меню",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 160,
            arcade.color.RED, 18,
            anchor_x="center"
        )
        self.top_texts = [
            arcade.Text("", SCREEN_WIDTH // 2, 0, arcade.color.WHITE, 18, anchor_x="center")
            for _ in range(3)
        ]

    def load_scores(self):
        with open("scores.csv", "r", encoding="utf-8") as f:
            return [line.strip().split(",") for line in f if line.strip()]

    def save_score(self):
        with open("scores.csv", "a", encoding="utf-8") as f:
            f.write(f"{self.nickname},{self.level},{self.score}\n")

    def on_draw(self):
        self.clear()

        self.title.draw()
        self.score_label.draw()

        if self.typing:
            self.input_prompt.draw()
            self.nickname_text.text = self.nickname + "▌"
            self.nickname_text.draw()
        else:
            self.leaderboard_title.draw()
            top = sorted(self.scores, key=lambda x: int(x[2]), reverse=True)[:3]
            for i, (name, lvl, sc) in enumerate(top):
                y = SCREEN_HEIGHT // 2 + 20 - i * 40
                self.top_texts[i].text = f"{i + 1}. {name} — {sc}"
                self.top_texts[i].position = (SCREEN_WIDTH // 2, y)
                self.top_texts[i].draw()

            self.next_hint.draw()
            self.menu_hint.draw()

    def on_key_press(self, key, modifiers):
        from views.menu_view import MenuView
        from views.game_view import GameView

        if self.typing:
            if key == arcade.key.ENTER and len(self.nickname) > 0:
                self.typing = False
                self.save_score()
            elif key == arcade.key.BACKSPACE:
                self.nickname = self.nickname[:-1]
            elif 32 <= key <= 126 and len(self.nickname) < 10:
                self.nickname += chr(key)
        else:
            if key == arcade.key.ENTER:
                if self.level == 2:
                    self.window.show_view(MenuView())
                else:
                    self.window.show_view(GameView(level=self.level + 1))
            elif key == arcade.key.ESCAPE:
                self.window.show_view(MenuView())
