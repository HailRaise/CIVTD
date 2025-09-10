import arcade

class UpgradePathMenu:
    def __init__(self, screen_width, screen_height, ui_bar_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ui_bar_height = ui_bar_height
        self.visible = False
        self.target_x = screen_width  # Start off-screen to the RIGHT
        self.current_x = screen_width  # Start off-screen to the RIGHT
        self.width = 350
        self.height = screen_height - ui_bar_height
        self.selected_tower = None
        self.animation_speed = 15
        self.tower_sprite = None
        
        # Upgrade paths with descriptions
        self.paths = [
            {"name": "Damage", "key": "damage", "color": arcade.color.RED, "description": "High firepower, short reach"},
            {"name": "Range", "key": "range", "color": arcade.color.GREEN, "description": "Longer attack radius"},
            {"name": "Speed", "key": "speed", "color": arcade.color.YELLOW, "description": "Attack faster"},
            {"name": "Gamble", "key": "gamble", "color": arcade.color.PURPLE, "description": "Random risky upgrade"}
        ]

    def show(self, tower):
        """Show the upgrade path menu"""
        self.selected_tower = tower
        self.tower_image_path = tower.image_path
        self.tower_scale = 0.5  # Reduced from 1.2 to 0.5
        
        try:
            self.tower_sprite = arcade.Sprite(self.tower_image_path, self.tower_scale)
        except:
            self.tower_sprite = arcade.Sprite(":resources:images/items/coinGold.png", 0.5)
        
        self.visible = True
        self.target_x = self.screen_width - self.width
    
    def hide(self):
        """Hide the menu"""
        self.visible = False
        self.target_x = self.screen_width   # Slide back off-screen to the right
        self.selected_tower = None
        self.tower_sprite = None
    
    def update(self):
        """Update menu animation"""
        if self.current_x < self.target_x:
            self.current_x += self.animation_speed
            if self.current_x > self.target_x:
                self.current_x = self.target_x
        elif self.current_x > self.target_x:
            self.current_x -= self.animation_speed
            if self.current_x < self.target_x:
                self.current_x = self.target_x
    
    def draw(self, money):
        """Draw the upgrade path menu"""
        # Change visibility check for right-side positioning
        if not self.visible and self.current_x >= self.screen_width:
            return

        # Draw background
        arcade.draw_lbwh_rectangle_filled(
            self.current_x, self.ui_bar_height, self.width, self.height,
            arcade.color.DARK_SLATE_GRAY
        )

        # Draw border
        arcade.draw_lbwh_rectangle_outline(
            self.current_x, self.ui_bar_height, self.width, self.height,
            arcade.color.WHITE, 2
        )

        if self.selected_tower and self.tower_sprite:
            # Draw tower sprite/info at top of menu
            self.tower_sprite.center_x = self.current_x + self.width / 2
            self.tower_sprite.center_y = self.screen_height - 80
            arcade.draw_sprite(self.tower_sprite)

            arcade.draw_text(
                f"{self.selected_tower.tower_type.capitalize()} Tower",
                self.current_x + 20, self.screen_height - 120,
                arcade.color.WHITE, 20
            )

            arcade.draw_text(
                f"Level: {self.selected_tower.level}/{self.selected_tower.max_level}",
                self.current_x + 20, self.screen_height - 150,
                arcade.color.WHITE, 16
            )

            # --- Draw upgrade path buttons ---
            button_area_height = self.height - 200
            button_spacing = button_area_height // len(self.paths)
            path_y_start = self.ui_bar_height + button_area_height - 40

            for i, path in enumerate(self.paths):
                path_y = path_y_start - (i * button_spacing)

                upgrade_cost = self.selected_tower.get_upgrade_cost()
                can_afford = money >= upgrade_cost

                # Draw path button background
                arcade.draw_lbwh_rectangle_filled(
                    self.current_x + 25, path_y - 40, 300, 80,
                    path["color"] if can_afford else arcade.color.GRAY
                )

                # Path name
                arcade.draw_text(
                    path["name"], self.current_x + 40, path_y,
                    arcade.color.WHITE, 20
                )

                # Cost
                arcade.draw_text(
                    f"${upgrade_cost}", self.current_x + 240, path_y,
                    arcade.color.WHITE, 18
                )

                # Description
                arcade.draw_text(
                    path["description"], self.current_x + 40, path_y - 20,
                    arcade.color.LIGHT_GRAY, 12
                )

                # Stat preview
                next_stats = self.selected_tower.get_next_level_stats(path["key"])
                if next_stats:
                    stats_text = (f"Dmg:{next_stats['damage']}  "
                                f"Rng:{next_stats['range']}  "
                                f"Spd:{next_stats['attack_speed']:.2f}")
                    arcade.draw_text(
                        stats_text, self.current_x + 40, path_y - 35,
                        arcade.color.WHITE, 10
                    )
    
    def check_click(self, x, y):
        """Check if any path button was clicked"""
        # Change visibility check for right-side positioning
        if not self.visible or self.current_x >= self.screen_width:
            return None

        menu_x = x - self.current_x
        if menu_x < 0 or menu_x > self.width or y < self.ui_bar_height or y > self.screen_height:
            return None

        # Use same layout math as draw()
        button_area_height = self.height - 200
        button_spacing = button_area_height // len(self.paths)
        path_y_start = self.ui_bar_height + button_area_height - 40

        for i, path in enumerate(self.paths):
            path_y = path_y_start - (i * button_spacing)
            if (25 <= menu_x <= 325 and path_y - 40 <= y <= path_y + 40):
                if path["key"] == "gamble":
                    return "gamble_minigame"  
                return path["key"]

        return None