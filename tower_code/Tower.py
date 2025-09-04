# core/tower.py
import arcade

class Tower(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("assets/towers/basic_tower.png", scale=1.0)
        self.center_x = x
        self.center_y = y
