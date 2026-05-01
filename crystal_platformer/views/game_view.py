import arcade


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass
