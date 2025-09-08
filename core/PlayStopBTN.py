import arcade

class PlayPauseButton:
    def __init__(self, x, y, width=80, height=40):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_paused = False
        
    def draw(self):
        """Draw the play/pause button"""
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        
        # Draw button background
        arcade.draw_lbwh_rectangle_filled(
            center_x,
            center_y,
            self.width,
            self.height,
            arcade.color.DARK_GRAY
        )
        
        # Draw button border
        arcade.draw_lbwh_rectangle_outline(
            center_x,
            center_y,
            self.width,
            self.height,
            arcade.color.WHITE,
            border_width=2
        )
        
        # Draw play or pause icon
        if self.is_paused:
            # Draw play icon (right-facing triangle) - CORRECTED
            arcade.draw_triangle_filled(
                center_x - 8, center_y - 10,  # x1, y1 (bottom left)
                center_x - 8, center_y + 10,  # x2, y2 (top left) 
                center_x + 10, center_y,      # x3, y3 (right tip)
                arcade.color.GREEN            # color
            )
            # Draw "PAUSED" text above button
            arcade.draw_text("PAUSED", center_x - 30, self.y + self.height + 10, 
                           arcade.color.RED, 16)
        else:
            # Draw pause icon (two vertical bars)
            arcade.draw_lbwh_rectangle_filled(center_x - 8, center_y, 6, 20, arcade.color.RED)
            arcade.draw_lbwh_rectangle_filled(center_x + 8, center_y, 6, 20, arcade.color.RED)
    
    def check_click(self, x, y):
        """Check if the button was clicked"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def toggle(self):
        """Toggle play/pause state"""
        self.is_paused = not self.is_paused
        return self.is_paused