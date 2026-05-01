import arcade
from pyglet.graphics import Batch
from crystal_platformer.constants import BG_COLOR, TEXT_COLOR, MENU_TITLE_SIZE, MENU_HINT_SIZE, SCREEN_WIDTH, \
    SCREEN_HEIGHT
from views.game_view import GameView


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = BG_COLOR

        self.batch = Batch()
        self.main_text = arcade.Text("Главное Меню", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                                     TEXT_COLOR, font_size=MENU_TITLE_SIZE, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы начать!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                                      TEXT_COLOR, font_size=MENU_HINT_SIZE, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = GameView()
            self.window.show_view(game_view)
