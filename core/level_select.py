# core/level_select.py
import arcade
from core.constants import *

class LevelSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.hovered_level = None
        self.levels = [
            {"name": "Level 1", "map_path": "assets/maps/first_round_map_obj.tmx", "unlocked": True},
            {"name": "Level 2", "map_path": "assets/maps/level2.tmx", "unlocked": False},
            {"name": "Level 3", "map_path": "assets/maps/level3.tmx", "unlocked": False}
        ]
        
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        
    def on_draw(self):
        self.clear()
        arcade.draw_text("SELECT LEVEL", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100,
                        arcade.color.WHITE, font_size=40, anchor_x="center")
        
        for i, level in enumerate(self.levels):
            y_pos = SCREEN_HEIGHT // 2 - (i * 100)
            color = arcade.color.GREEN if level["unlocked"] else arcade.color.GRAY
            
            # Draw level button using lbwh coordinates
            left = SCREEN_WIDTH // 2 - 150
            bottom = y_pos - 40
            arcade.draw_lbwh_rectangle_filled(left, bottom, 300, 80, color)
            
            arcade.draw_text(level["name"], SCREEN_WIDTH // 2, y_pos,
                           arcade.color.WHITE, font_size=25, anchor_x="center", anchor_y="center")
            
            if self.hovered_level is not None:
                y_pos = SCREEN_HEIGHT // 2 - (self.hovered_level * 100)
                left = SCREEN_WIDTH // 2 - 150
                bottom = y_pos - 40
                arcade.draw_lbwh_rectangle_outline(
                    left, bottom, 300, 80, arcade.color.YELLOW, border_width=3
                )
    
    def on_mouse_press(self, x, y, button, modifiers):
        for i, level in enumerate(self.levels):
            y_pos = SCREEN_HEIGHT // 2 - (i * 100)
            left = SCREEN_WIDTH // 2 - 150
            right = left + 300
            bottom = y_pos - 40
            top = bottom + 80
            
            if (left <= x <= right and bottom <= y <= top and level["unlocked"]):
                from core.game_view import TowerDefenseGame
                game_view = TowerDefenseGame(level["map_path"])
                self.window.show_view(game_view)
                break
    def on_mouse_motion(self, x, y, dx, dy):
        """Highlight buttons on hover"""
        self.hovered_level = None
        for i, level in enumerate(self.levels):
            y_pos = SCREEN_HEIGHT // 2 - (i * 100)
            left = SCREEN_WIDTH // 2 - 150
            right = left + 300
            bottom = y_pos - 40
            top = bottom + 80
            
            if (left <= x <= right and bottom <= y <= top and level["unlocked"]):
                self.hovered_level = i
                break


        