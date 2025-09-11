# core/level_select.py
import arcade
from core.constants import *
from core.LevelManager import LevelManager
from core.game_view import TowerDefenseGame

class LevelSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.hovered_level = None
        self.manager = LevelManager()
        self.levels = list(self.manager.levels.items())  # [(1, LevelData), (2, LevelData), ...]

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text("SELECT LEVEL", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100,
                         arcade.color.WHITE, font_size=40, anchor_x="center")

        for i, (level_num, level_data) in enumerate(self.levels):
            y_pos = SCREEN_HEIGHT // 2 - (i * 100)
            color = arcade.color.GREEN  # you can add locked/unlocked logic later

            left = SCREEN_WIDTH // 2 - 150
            bottom = y_pos - 40
            arcade.draw_lbwh_rectangle_filled(left, bottom, 300, 80, color)

            arcade.draw_text(f"Level {level_num}", SCREEN_WIDTH // 2, y_pos,
                             arcade.color.WHITE, font_size=25,
                             anchor_x="center", anchor_y="center")

            if self.hovered_level == i:
                arcade.draw_lbwh_rectangle_outline(left, bottom, 300, 80,
                                                   arcade.color.YELLOW, border_width=3)

    def on_mouse_press(self, x, y, button, modifiers):
        for i, (level_num, level_data) in enumerate(self.levels):
            y_pos = SCREEN_HEIGHT // 2 - (i * 100)
            left = SCREEN_WIDTH // 2 - 150
            right = left + 300
            bottom = y_pos - 40
            top = bottom + 80

            if left <= x <= right and bottom <= y <= top:
                game_view = TowerDefenseGame(level_data)
                self.window.show_view(game_view)
                break

    def on_mouse_motion(self, x, y, dx, dy):
        self.hovered_level = None
        for i, (level_num, level_data) in enumerate(self.levels):
            y_pos = SCREEN_HEIGHT // 2 - (i * 100)
            left = SCREEN_WIDTH // 2 - 150
            right = left + 300
            bottom = y_pos - 40
            top = bottom + 80
            if left <= x <= right and bottom <= y <= top:
                self.hovered_level = i
                break
