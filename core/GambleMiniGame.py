import arcade
import random
import math
from core.constants import *

class GambleMiniGame:
    def __init__(self, screen_width, screen_height, ui_bar_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ui_bar_height = ui_bar_height
        self.visible = False
        self.width = 500
        self.height = 400
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2
        self.tower = None
        self.money_ref = None  # Reference to money variable
        self.result = None
        self.spinning = False
        self.spin_timer = 0
        self.spin_angle = 0
        self.wheel_options = [
            {"text": "DOUBLE", "color": arcade.color.GREEN, "angle": 0, "weight": 0.2},
            {"text": "HALF", "color": arcade.color.RED, "angle": 72, "weight": 0.3},
            {"text": "NOTHING", "color": arcade.color.GRAY, "angle": 144, "weight": 0.3},
            {"text": "FREE", "color": arcade.color.BLUE, "angle": 216, "weight": 0.15},
            {"text": "MAX", "color": arcade.color.GOLD, "angle": 288, "weight": 0.05}
        ]
        self.selected_option = None
        self.animation_phase = 0  # 0=waiting, 1=spinning, 2=result
        
    def show(self, tower, money_ref):
        """Show the gamble minigame"""
        self.tower = tower
        self.money_ref = money_ref
        self.visible = True
        self.result = None
        self.spinning = False
        self.spin_angle = 0
        self.selected_option = None
        self.animation_phase = 0
        
    def hide(self):
        """Hide the minigame"""
        self.visible = False
        self.tower = None
        self.money_ref = None
        self.result = None
        
    def spin(self):
        """Start the spin animation"""
        if not self.spinning and self.animation_phase == 0:
            self.spinning = True
            self.animation_phase = 1
            self.spin_timer = 0
            self.result = None
            self.selected_option = None
            
    def update(self, delta_time):
        """Update minigame animation"""
        if self.spinning:
            self.spin_timer += delta_time
            self.spin_angle += delta_time * 720  # Spin speed
            
            # Slow down after 2 seconds
            if self.spin_timer >= 2.0:
                spin_speed = max(10, 720 * (1 - (self.spin_timer - 2.0) * 2))
                self.spin_angle += delta_time * spin_speed
                
                # Stop spinning after 3 seconds
                if self.spin_timer >= 3.0:
                    self.spinning = False
                    self.determine_result()
                    self.animation_phase = 2
                    
    def determine_result(self):
        """Determine the random result based on wheel position"""
        # Get final angle (normalized to 0-360)
        final_angle = self.spin_angle % 360
        
        # Find which segment the pointer landed on
        for option in self.wheel_options:
            segment_start = option["angle"]
            segment_end = (option["angle"] + 72) % 360
            
            if segment_start <= segment_end:
                if segment_start <= final_angle < segment_end:
                    self.selected_option = option
                    break
            else:  # Handle wrap-around
                if final_angle >= segment_start or final_angle < segment_end:
                    self.selected_option = option
                    break
        
        if self.selected_option:
            self.result = self.selected_option["text"]
            self.apply_result()
            
    def apply_result(self):
        """Apply the gamble result to the tower"""
        if self.result == "DOUBLE":
            # Double all stats
            self.tower.properties["damage"] *= 2
            self.tower.properties["range"] *= 2
            self.tower.properties["attack_speed"] *= 2
            print("🎉 DOUBLE! All stats doubled!")
            
        elif self.result == "HALF":
            # Halve all stats
            self.tower.properties["damage"] *= 0.5
            self.tower.properties["range"] *= 0.5
            self.tower.properties["attack_speed"] *= 0.5
            print("💔 HALF! All stats halved!")
            
        elif self.result == "NOTHING":
            # No change
            print("😐 NOTHING! No changes made.")
            
        elif self.result == "FREE":
            # Free upgrade, refund money
            refund = self.tower.get_upgrade_cost()
            self.money_ref[0] += refund  # Refund the cost
            print(f"🎁 FREE! ${refund} refunded!")
            
        elif self.result == "MAX":
            # Max out the tower (simplified)
            bonus = 5
            self.tower.properties["damage"] += bonus
            self.tower.properties["range"] += bonus * 20
            self.tower.properties["attack_speed"] += bonus * 0.5
            print(f"🔥 MAX! +{bonus} to all stats!")
    
    def check_click(self, x, y):
        """Check if spin button was clicked"""
        if not self.visible:
            return False
            
        # Check spin button
        spin_button_x = self.center_x
        spin_button_y = self.center_y - 50
        spin_button_width = 100
        spin_button_height = 40
        
        if (spin_button_x - spin_button_width//2 <= x <= spin_button_x + spin_button_width//2 and
            spin_button_y - spin_button_height//2 <= y <= spin_button_y + spin_button_height//2):
            if self.animation_phase == 0:  # Only allow click if not spinning
                self.spin()
                return True
                
        return False
        
    def draw(self):
        """Draw the minigame"""
        if not self.visible:
            return
            
        # Draw semi-transparent overlay
        arcade.draw_lbwh_rectangle_filled(
            0, 0, self.screen_width, self.screen_height,
            (0, 0, 0, 180)  # Semi-transparent black
        )
        
        # Draw game window
        arcade.draw_lbwh_rectangle_filled(
            self.center_x - self.width // 2,
            self.center_y - self.height // 2,
            self.width,
            self.height,
            arcade.color.DARK_SLATE_GRAY
        )
        
        # Draw border
        arcade.draw_lbwh_rectangle_outline(
            self.center_x - self.width // 2,
            self.center_y - self.height // 2,
            self.width,
            self.height,
            arcade.color.GOLD,
            4
        )
        
        # Draw title
        arcade.draw_text(
            "🎲 GAMBLE MINIGAME 🎲",
            self.center_x,
            self.center_y + self.height // 2 - 30,
            arcade.color.GOLD,
            28,
            anchor_x="center",
            bold=True
        )
        
        # Draw wheel
        wheel_radius = 120
        wheel_x = self.center_x
        wheel_y = self.center_y + 20
        
        # Draw wheel segments
        for option in self.wheel_options:
            angle = option["angle"] + self.spin_angle
            arcade.draw_arc_filled(
                wheel_x, wheel_y, wheel_radius, wheel_radius,
                option["color"], angle, angle + 72, 0
            )
            
            # Draw segment text
            text_angle = math.radians(angle + 36)
            text_x = wheel_x + math.cos(text_angle) * wheel_radius * 0.7
            text_y = wheel_y + math.sin(text_angle) * wheel_radius * 0.7
            
            arcade.draw_text(
                option["text"],
                text_x, text_y,
                arcade.color.WHITE,
                12,
                anchor_x="center",
                anchor_y="center",
                rotation=angle + 36
            )
        
        # Draw wheel center and pointer
        arcade.draw_circle_filled(wheel_x, wheel_y, 10, arcade.color.BLACK)
        arcade.draw_line(
            wheel_x, wheel_y + wheel_radius + 10,
            wheel_x, wheel_y + wheel_radius - 10,
            arcade.color.RED, 3
        )
        
        # Draw spin button
        button_color = arcade.color.RED if self.animation_phase == 0 else arcade.color.GRAY
        arcade.draw_lbwh_rectangle_filled(
            self.center_x, self.center_y - 100,
            120, 40, button_color
        )
        
        button_text = "SPIN" if self.animation_phase == 0 else "SPINNING..." if self.animation_phase == 1 else "SPIN AGAIN"
        arcade.draw_text(
            button_text,
            self.center_x, self.center_y - 100,
            arcade.color.WHITE,
            30,
            anchor_x="center",
            anchor_y="center"
        )
        
        # Draw result if available
        if self.result and self.animation_phase == 2:
            result_color = arcade.color.GREEN
            if self.result == "HALF":
                result_color = arcade.color.RED
            elif self.result == "NOTHING":
                result_color = arcade.color.GRAY
                
            arcade.draw_text(
                f"RESULT: {self.result}",
                self.center_x,
                self.center_y - 150,
                result_color,
                24,
                anchor_x="center",
                bold=True
            )
            
            # Draw instructions to continue
            arcade.draw_text(
                "Click anywhere to continue",
                self.center_x,
                self.center_y - 180,
                arcade.color.WHITE,
                16,
                anchor_x="center"
            )