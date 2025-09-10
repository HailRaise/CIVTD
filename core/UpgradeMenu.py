import arcade

class UpgradeMenu:
    def __init__(self, screen_width, screen_height, ui_bar_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ui_bar_height = ui_bar_height
        self.visible = False
        self.target_x = screen_width
        self.current_x = screen_width
        self.width = 250
        self.height = screen_height - ui_bar_height
        self.selected_tower = None
        self.animation_speed = 15
        self.tower_sprite = None
        
        # Create buttons
        self.upgrade_button = {
            'x': 20, 'y': 150, 'width': 200, 'height': 50,
            'text': "Upgrade", 'visible': True
        }
        self.sell_button = {
            'x': 20, 'y': 80, 'width': 200, 'height': 50,
            'text': "Sell", 'visible': True
        }
        self.close_button = {
            'x': 20, 'y': 20, 'width': 200, 'height': 40,
            'text': "Close", 'visible': True
        }
    
    def show(self, tower):
        """Show the menu for a specific tower"""
        self.selected_tower = tower
        
        # Use the image path stored in the tower
        self.tower_image_path = tower.image_path
        
        # Handle scale - REDUCE the scaling factor
        if hasattr(tower, 'scale'):
            if isinstance(tower.scale, (tuple, list)):
                # Use a much smaller scale for the menu
                self.tower_scale = tower.scale[0] * 0.5  # Reduced from 1.5 to 0.5
            else:
                # Use a much smaller scale for the menu
                self.tower_scale = tower.scale * 0.5  # Reduced from 1.5 to 0.5
        else:
            # Fallback if scale attribute doesn't exist
            self.tower_scale = 0.8  # Reduced from 1.5
        
        print(f"Tower scale: {tower.scale} (type: {type(tower.scale)})")
        print(f"Menu scale: {self.tower_scale}")
        
        # Create the sprite for the menu
        try:
            self.tower_sprite = arcade.Sprite(self.tower_image_path, self.tower_scale)
            print(f"Loaded sprite from: {self.tower_image_path}")
        except Exception as e:
            print(f"Error loading sprite {self.tower_image_path}: {e}")
            # Fallback: use a default sprite
            self.tower_sprite = arcade.Sprite(":resources:images/items/coinGold.png", 0.5)
        
        self.visible = True
        self.target_x = self.screen_width - self.width
    
    def hide(self):
        """Hide the menu"""
        self.visible = False
        self.target_x = self.screen_width
        self.selected_tower = None
        self.tower_sprite = None
    
    def update(self):
        """Update menu animation"""
        # Smooth sliding animation
        if self.current_x < self.target_x:
            self.current_x += self.animation_speed
            if self.current_x > self.target_x:
                self.current_x = self.target_x
        elif self.current_x > self.target_x:
            self.current_x -= self.animation_speed
            if self.current_x < self.target_x:
                self.current_x = self.target_x
    
    def draw(self, money):
        """Draw the menu"""
        if not self.visible and self.current_x >= self.screen_width:
            return
            
        # Draw background using lbwh (left, bottom, width, height)
        arcade.draw_lbwh_rectangle_filled(
            self.current_x,  # left
            self.ui_bar_height,  # bottom
            self.width,  # width
            self.height,  # height
            arcade.color.DARK_SLATE_GRAY
        )
        
        # Draw border using lbwh
        arcade.draw_lbwh_rectangle_outline(
            self.current_x,  # left
            self.ui_bar_height,  # bottom
            self.width,  # width
            self.height,  # height
            arcade.color.WHITE,
            border_width=2
        )
        
        if self.selected_tower and self.tower_sprite:
            # Draw tower sprite at the top of the menu
            self.tower_sprite.center_x = self.current_x + self.width / 2
            self.tower_sprite.center_y = self.screen_height - 80
            arcade.draw_sprite(self.tower_sprite)
            
            # Draw tower info below the sprite
            info_y_start = self.screen_height - 120
            
            arcade.draw_text(
                f"{self.selected_tower.tower_type.capitalize()} Tower",
                self.current_x + 20,
                info_y_start,
                arcade.color.WHITE,
                20
            )
            
            arcade.draw_text(
                f"Level: {self.selected_tower.level}/{self.selected_tower.max_level}",
                self.current_x + 20,
                info_y_start - 30,
                arcade.color.WHITE,
                16
            )
            
            arcade.draw_text(
                f"Damage: {self.selected_tower.properties['damage']}",
                self.current_x + 20,
                info_y_start - 60,
                arcade.color.WHITE,
                16
            )
            
            arcade.draw_text(
                f"Range: {self.selected_tower.properties['range']}",
                self.current_x + 20,
                info_y_start - 90,
                arcade.color.WHITE,
                16
            )
            
            arcade.draw_text(
                f"Speed: {self.selected_tower.properties['attack_speed']:.1f}/s",
                self.current_x + 20,
                info_y_start - 120,
                arcade.color.WHITE,
                16
            )
            
            # Draw buttons using lbwh
            button_y_start = self.ui_bar_height + self.height - 500
            
            # Upgrade button (only show if can upgrade)
            upgrade_bottom = button_y_start - 50
            if self.selected_tower.can_upgrade():
                upgrade_cost = self.selected_tower.get_upgrade_cost()
                can_afford = money >= upgrade_cost
                button_color = arcade.color.GREEN if can_afford else arcade.color.RED
                
                # Draw upgrade button using lbwh
                arcade.draw_lbwh_rectangle_filled(
                    self.current_x + 25,  # left
                    button_y_start - 50,  # bottom
                    200,  # width
                    50,  # height
                    button_color
                )
                
                arcade.draw_text(
                    f"Upgrade (${upgrade_cost})",
                    self.current_x + 40,
                    button_y_start - 25,
                    arcade.color.WHITE,
                    16
                )
                
                # Show next level stats preview
                next_stats = self.selected_tower.get_next_level_stats()
                if next_stats:
                    arcade.draw_text(
                        f"Next: Dmg:{next_stats['damage']} Rng:{next_stats['range']}",
                        self.current_x + 20,
                        button_y_start - 70,
                        arcade.color.LIGHT_GREEN,
                        12
                    )
            elif self.selected_tower.level == self.selected_tower.max_level:
                # Tower is at MAX level - show grayed out message
                arcade.draw_lbwh_rectangle_filled(
                    self.current_x + 25, upgrade_bottom, 200, 50, arcade.color.GRAY
                )
                
                arcade.draw_text(
                    "MAX LEVEL REACHED",
                    self.current_x + 30,
                    upgrade_bottom + 25, 
                    arcade.color.WHITE,
                    16
                )
            else:
                print("DEBUG: Tower exists but cannot be upgraded yet")
                # DON'T DRAW ANYTHING HERE or draw a disabled button
                # This prevents the max level text from appearing when it shouldn't
                arcade.draw_lbwh_rectangle_filled(
                    self.current_x + 25, button_y_start - 50, 200, 50, arcade.color.DARK_GRAY
                )
                
                arcade.draw_text(
                    "Cannot Upgrade Yet",
                    self.current_x + 40,
                    button_y_start - 25,
                    arcade.color.LIGHT_GRAY,
                    16
                )
            
            
            # Sell button using lbwh
            sell_value = self.selected_tower.get_sell_value()
            arcade.draw_lbwh_rectangle_filled(
                self.current_x + 25,
                button_y_start - 110,
                200,
                50,
                arcade.color.ORANGE
            )
            
            arcade.draw_text(
                f"Sell (${sell_value})",
                self.current_x + 60,
                button_y_start - 85,
                arcade.color.WHITE,
                16
            )
            
            # Close button using lbwh
            arcade.draw_lbwh_rectangle_filled(
                self.current_x + 25,
                button_y_start - 170,
                200,
                40,
                arcade.color.DARK_BLUE
            )
            
            arcade.draw_text(
                "Close",
                self.current_x + 85,
                button_y_start - 155,
                arcade.color.WHITE,
                16
            )
    
    def check_click(self, x, y):
        """Check if any menu button was clicked"""
        if not self.visible or self.current_x >= self.screen_width:
            return None
            
        # Convert click position to menu coordinates
        menu_x = x - self.current_x
        
        # Only check clicks that are actually within the menu bounds
        if menu_x < 0 or menu_x > self.width or y < self.ui_bar_height or y > self.screen_height:
            return None
        
        # Calculate button positions based on the new layout
        button_y_start = self.ui_bar_height + self.height - 500
        
        # Check upgrade button (if available)
        if self.selected_tower and self.selected_tower.can_upgrade():
            upgrade_bottom = button_y_start - 50
            upgrade_top = button_y_start
            if (25 <= menu_x <= 225 and 
                upgrade_bottom <= y <= upgrade_top):
                print(f"Click in upgrade area: {25 <= menu_x <= 225 and upgrade_bottom <= y <= upgrade_top}")
                return "upgrade"
        
        # Check sell button
        sell_bottom = button_y_start - 110
        sell_top = button_y_start - 60
        if (25 <= menu_x <= 225 and 
            sell_bottom <= y <= sell_top):
            return "sell"
        
        # Check close button
        close_bottom = button_y_start - 170
        close_top = button_y_start - 130
        if (25 <= menu_x <= 225 and 
            close_bottom <= y <= close_top):
            return "close"
            
        return None