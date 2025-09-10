# core/MainMenu.py
import arcade
from core.constants import *

class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.buttons = [
            {"text": "Start Game", "y": 400, "width": 300, "height": 60, "action": "level_select"},
            {"text": "Quit", "y": 300, "width": 300, "height": 60, "action": "quit"}
        ]
        
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        
    def on_draw(self):
        self.clear()
        arcade.draw_text("GAMBLING TOWER DEFENSE", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100,
                        arcade.color.WHITE, font_size=50, anchor_x="center")
        
        for button in self.buttons:
            left = SCREEN_WIDTH // 2 - button["width"] // 2
            bottom = button["y"] - button["height"] // 2
            
            arcade.draw_lbwh_rectangle_filled(
                left, bottom, button["width"], button["height"], arcade.color.DARK_GREEN
            )
            arcade.draw_text(
                button["text"], SCREEN_WIDTH // 2, button["y"],
                arcade.color.WHITE, font_size=30, anchor_x="center", anchor_y="center"
            )
    
    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            left = SCREEN_WIDTH // 2 - btn["width"] // 2
            right = left + btn["width"]
            bottom = btn["y"] - btn["height"] // 2
            top = bottom + btn["height"]
            
            if (left <= x <= right and bottom <= y <= top):
                if btn["action"] == "level_select":
                    from core.level_select import LevelSelectView
                    level_view = LevelSelectView()
                    self.window.show_view(level_view)
                elif btn["action"] == "quit":
                    arcade.close_window()
                break