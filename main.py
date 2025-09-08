import arcade
from core.map_loader import load_map_and_path
from enemy_code.enemy import Enemy
from core.enemy_spawner import spawn_enemy
from tower_code.TowerMenu import TowerMenuClass   
from tower_code.Tower import Tower
from core.PlayStopBTN import PlayPauseButton
from core.UpgradeMenu import UpgradeMenu
from core.UpgradePathMenu import UpgradePathMenu
import math

SCREEN_WIDTH = 1200
UI_BAR_HEIGHT = 150
SCREEN_HEIGHT = 950
SCREEN_TITLE = "Tower Defense Starter"
TILE_SCALING = 1.0
TOWER_RANGE = 120
TOWER_COLLISION_RADIUS = 24
ROAD_BLOCK_RADIUS = 28     
MAP_PATH = "assets/maps/first_round_map_obj.tmx"

class TowerDefense(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        self.money = 1000  # Add money system
        
        self.hovered_tower_type = None 
        self.mouse_x = 0  # Track mouse position
        self.mouse_y = 0
        self.active_tower = None
        self.ghost_tower = None
        self.selected_tower_type = None
        self.selected_tower_image = None
        self.selected_tower_scale = None

        self.play_pause_button = None
        self.upgrade_menu = None
        
        self.play_pause_button = PlayPauseButton(
        SCREEN_WIDTH - 100,  # x position
        UI_BAR_HEIGHT - 50,  # y position
        80,  # width
        40   # height
        )
        self.upgrade_path_menu = UpgradePathMenu(SCREEN_WIDTH, SCREEN_HEIGHT, UI_BAR_HEIGHT)
        
        # Setup will be called after initialization
        self.setup()

    def setup(self):
        """Set up the game"""
        # --- Load map and scene, extract spawn and path ---
        self.tile_map, self.scene, self.spawn_point, self.enemy_path = load_map_and_path(MAP_PATH, TILE_SCALING)

        # --- Set up enemy list ---
        self.scene.add_sprite_list("Enemies", use_spatial_hash=True)
        self.enemy_spawn_timer = 0.0
        self.enemies_spawned = 0
        self.total_enemies_to_spawn = 15

        # Setup towers
        self.tower_menu = TowerMenuClass(UI_BAR_HEIGHT)
        self.scene.add_sprite_list("Towers")
        self.tower_menu.add_icon("assets/free-archer-towers-pixel-art-for-tower-defense/1 Upgrade/first_build.png", 60, "basic")
        self.upgrade_menu = UpgradeMenu(SCREEN_WIDTH, SCREEN_HEIGHT, UI_BAR_HEIGHT)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """Update mouse position and handle hover effects"""
        self.mouse_x = x
        self.mouse_y = y
        
        # Update ghost tower position to follow mouse
        if self.ghost_tower and y > UI_BAR_HEIGHT:
            self.ghost_tower.center_x = x
            self.ghost_tower.center_y = y
            
        # Check if hovering over tower menu icons
        hovered_icons = arcade.get_sprites_at_point((x, y), self.tower_menu.icons)
        self.hovered_tower_type = None
        
        if hovered_icons:
            hovered_icon = hovered_icons[-1]
            self.hovered_tower_type = hovered_icon.properties["type"]

    def on_draw(self):
        self.clear()
        self.scene.draw()
        
        # Draw enemies (they handle their own drawing including death animations)
        for enemy in self.scene["Enemies"]:
            enemy.draw()
        
        # Draw towers
        self.scene["Towers"].draw()
        
        # Draw tower ranges for selected towers
        for tower in self.scene["Towers"]:
            if hasattr(tower, 'show_range') and tower.show_range:
                arcade.draw_circle_outline(
                    tower.center_x,
                    tower.center_y,
                    tower.properties.get("range", TOWER_RANGE),
                    arcade.color.YELLOW,
                    border_width=3
                )
        
        # Draw tower projectiles and attack effects
        for tower in self.scene["Towers"]:
            tower.projectiles.draw()
            tower.draw_attack_effect()
        
        # Draw ghost tower if it exists
        if self.ghost_tower:
            arcade.draw_sprite(self.ghost_tower)
            
            # Draw range for ghost tower
            if hasattr(self.ghost_tower, 'properties'):
                arcade.draw_circle_outline(
                    self.ghost_tower.center_x,
                    self.ghost_tower.center_y,
                    self.ghost_tower.properties.get("range", TOWER_RANGE),
                    arcade.color.LIGHT_GRAY,
                    border_width=2
                )
        
        # Draw range preview when hovering over menu icons
        if self.hovered_tower_type and self.mouse_y > UI_BAR_HEIGHT:
            # Create a temporary tower to get properties
            temp_tower = Tower(self.hovered_tower_type, "", 1.0)
            arcade.draw_circle_outline(
                self.mouse_x,
                self.mouse_y,
                temp_tower.properties.get("range", TOWER_RANGE),
                arcade.color.LIGHT_GRAY,
                border_width=1
            )
            
            # Draw range text
            arcade.draw_text(
                f"Range: {temp_tower.properties.get('range', TOWER_RANGE)}",
                self.mouse_x + 20,
                self.mouse_y - 20,
                arcade.color.WHITE,
                12
            )
        
        # Draw UI bar
        arcade.draw_lbwh_rectangle_filled(
            0,                # left
            0,                # bottom
            SCREEN_WIDTH,     # width
            UI_BAR_HEIGHT,    # height
            arcade.color.DARK_SLATE_GRAY
        )
        
        # Draw money counter
        arcade.draw_text(f"Money: ${self.money}", 20, UI_BAR_HEIGHT - 30, arcade.color.WHITE, 20)
        
        self.tower_menu.draw()

        # Optional: draw the path
        for x, y in self.enemy_path:
            arcade.draw_circle_filled(x, y, 5, arcade.color.RED)

        # Draw play/pause button
        self.play_pause_button.draw()
        arcade.draw_text(
        f"Menu: Visible={self.upgrade_menu.visible}, X={self.upgrade_menu.current_x}",
        10, SCREEN_HEIGHT - 30, arcade.color.RED, 16
    )
        self.upgrade_menu.draw(self.money)

    def on_mouse_press(self, x, y, button, modifiers):
        # First, check if the user clicked the upgrade path menu
        if self.upgrade_path_menu.visible and self.upgrade_path_menu.current_x > -300:
            selected_path = self.upgrade_path_menu.check_click(x, y)
            if selected_path:
                tower = self.upgrade_path_menu.selected_tower
                upgrade_cost = tower.get_upgrade_cost()
                
                if self.money >= upgrade_cost:
                    self.money -= upgrade_cost
                    success = tower.upgrade(selected_path)
                    if success:
                        print(f"Upgraded {tower.tower_type} to level {tower.level} via {selected_path} path")
                        # Show upgraded stats
                        print(f"New stats - Damage: {tower.properties['damage']}, Range: {tower.properties['range']}, Speed: {tower.properties['attack_speed']:.1f}")
                else:
                    print(f"Not enough money for upgrade! Need ${upgrade_cost}, have ${self.money}")
                
                self.upgrade_path_menu.hide()
                return
        
        # Then check if the user clicked the main upgrade menu
        if self.upgrade_menu.visible and self.upgrade_menu.current_x > -200:
            menu_action = self.upgrade_menu.check_click(x, y)
            if menu_action:
                if menu_action == "upgrade":
                    # Show upgrade path selection instead of direct upgrade
                    if self.upgrade_menu.selected_tower.can_upgrade():
                        self.upgrade_path_menu.show(self.upgrade_menu.selected_tower)
                    else:
                        print("Tower is already at maximum level!")
                        
                elif menu_action == "sell":
                    # Sell the selected tower
                    sell_value = self.upgrade_menu.selected_tower.get_sell_value()
                    self.money += sell_value
                    self.scene["Towers"].remove(self.upgrade_menu.selected_tower)
                    self.upgrade_menu.hide()
                    print(f"Sold {self.upgrade_menu.selected_tower.tower_type} tower for ${sell_value}")
                    
                elif menu_action == "close":
                    # Close the menu
                    self.upgrade_menu.hide()
                    
                return
        
        # Check if clicking on tower menu icons (this should come BEFORE upgrade menu check)
        tower_clicked = arcade.get_sprites_at_point((x, y), self.tower_menu.icons)
        if tower_clicked:
            clicked_icon = tower_clicked[-1]
            
            # Close all menus when selecting new tower
            if self.upgrade_menu.visible:
                self.upgrade_menu.hide()
            if self.upgrade_path_menu.visible:
                self.upgrade_path_menu.hide()
            
            # Check if player can afford this tower
            tower_cost = clicked_icon.properties.get("cost", 100)
            if self.money < tower_cost:
                print(f"Not enough money! Need ${tower_cost}, have ${self.money}")
                return
                
            # Store the selected tower properties
            self.selected_tower_type = clicked_icon.properties["type"]
            self.selected_tower_image = clicked_icon.properties["image_path"]
            self.selected_tower_scale = clicked_icon.properties["scale"]
            
            # Create ghost tower
            self.ghost_tower = arcade.Sprite(
                self.selected_tower_image,
                self.selected_tower_scale
            )
            self.ghost_tower.alpha = 128  # 50% opacity
            self.ghost_tower.center_x = x
            self.ghost_tower.center_y = y
            
            # Add properties to ghost tower for range drawing
            temp_tower = Tower(
                self.selected_tower_type, 
                self.selected_tower_image, 
                self.selected_tower_scale
            )
            self.ghost_tower.properties = temp_tower.properties
            
            print(f"Selected tower: {self.selected_tower_type} at ({x}, {y})")
            self.active_tower = None  
            
            # Hide range for all towers when selecting a new tower
            for tower in self.scene["Towers"]:
                if hasattr(tower, 'show_range'):
                    tower.show_range = False
                    
            return

        # Check if clicking on an existing tower to select it
        existing_tower_clicked = arcade.get_sprites_at_point((x, y), self.scene["Towers"])
        if existing_tower_clicked:
            # Close all menus first
            if self.upgrade_menu.visible:
                self.upgrade_menu.hide()
            if self.upgrade_path_menu.visible:
                self.upgrade_path_menu.hide()
            
            # First, hide range for all towers
            for tower in self.scene["Towers"]:
                if hasattr(tower, 'show_range'):
                    tower.show_range = False
                    
            # Then show range for the clicked tower and open upgrade menu
            self.active_tower = existing_tower_clicked[-1]
            if hasattr(self.active_tower, 'show_range'):
                self.active_tower.show_range = True
            
            # Show upgrade menu for this tower
            self.upgrade_menu.show(self.active_tower)
            
            print(f"Selected tower: {self.active_tower.tower_type} (Level {self.active_tower.level})")
            
            # Clear any tower placement selection
            self.selected_tower_type = None
            self.ghost_tower = None
            if hasattr(self.tower_menu, 'selected_tower_type'):
                self.tower_menu.selected_tower_type = None
            
            return

        # If we have a ghost tower (tower selected) and click is ABOVE the UI bar
        if self.ghost_tower and y > UI_BAR_HEIGHT:
            # Close all menus
            if self.upgrade_menu.visible:
                self.upgrade_menu.hide()
            if self.upgrade_path_menu.visible:
                self.upgrade_path_menu.hide()
            
            # Create the actual tower using the Tower class
            new_tower = Tower(
                tower_type=self.selected_tower_type,
                image_path=self.selected_tower_image,
                scale=self.selected_tower_scale
            )
            new_tower.center_x = x
            new_tower.center_y = y
            
            # Deduct money for tower placement
            tower_cost = new_tower.get_cost()
            if self.money >= tower_cost:
                self.money -= tower_cost
                self.scene["Towers"].append(new_tower)
                print(f"Placed {self.selected_tower_type} tower at ({x}, {y}) for ${tower_cost}")
            else:
                print(f"Not enough money to place tower! Need ${tower_cost}, have ${self.money}")
            
            # Clear selection and ghost tower
            self.selected_tower_type = None
            self.ghost_tower = None
            if hasattr(self.tower_menu, 'selected_tower_type'):
                self.tower_menu.selected_tower_type = None
            
            # Hide range for all towers after placement
            for tower in self.scene["Towers"]:
                if hasattr(tower, 'show_range'):
                    tower.show_range = False
                    
            return

        # If clicking elsewhere (not on UI or tower), hide all ranges and menus
        elif y > UI_BAR_HEIGHT:
            for tower in self.scene["Towers"]:
                if hasattr(tower, 'show_range'):
                    tower.show_range = False
            self.active_tower = None
            if self.upgrade_menu.visible:
                self.upgrade_menu.hide()
            if self.upgrade_path_menu.visible:
                self.upgrade_path_menu.hide()
        

    def on_key_press(self, key, modifiers):
        """Handle key presses - ESC to cancel tower placement"""
        if key == arcade.key.ESCAPE:
            # Cancel tower placement
            self.ghost_tower = None
            self.selected_tower_type = None
            if hasattr(self.tower_menu, 'selected_tower_type'):
                self.tower_menu.selected_tower_type = None
            print("Tower placement cancelled")
        if key == arcade.key.SPACE:
            # Toggle play/pause with spacebar
            self.play_pause_button.toggle()
            print("Game", "paused" if self.play_pause_button.is_paused else "resumed")
            return
    

    def update_towers(self, delta_time):
        """Update all towers and handle their attacks"""
        for tower in self.scene["Towers"]:
            # Update the tower (cooldowns, etc.)
            tower.update(delta_time)
            
            # Get only living enemies (not dying ones) for targeting
            living_enemies = [e for e in self.scene["Enemies"] if hasattr(e, 'alive') and e.alive and not (hasattr(e, 'is_dying') and e.is_dying)]
            
            if living_enemies:
                # Make the tower attack if possible
                tower.attack(delta_time, living_enemies)
            
            # Update projectiles and check for hits
            for projectile in tower.projectiles:
                # Move projectile towards target
                if (projectile.properties["target"] and 
                    hasattr(projectile.properties["target"], 'alive') and
                    projectile.properties["target"].alive and
                    not (hasattr(projectile.properties["target"], 'is_dying') and projectile.properties["target"].is_dying)):
                    
                    target = projectile.properties["target"]
                    dx = target.center_x - projectile.center_x
                    dy = target.center_y - projectile.center_y
                    distance = math.sqrt(dx * dx + dy * dy)
                    
                    if distance > 0:
                        # Move projectile
                        speed = projectile.properties["speed"] * delta_time
                        projectile.center_x += (dx / distance) * speed
                        projectile.center_y += (dy / distance) * speed
                        
                        # Check if projectile hit target
                        if distance < 10:  # Hit threshold
                            target.take_damage(projectile.properties["damage"])
                            projectile.remove_from_sprite_lists()
                else:
                    # Target is dead or gone, remove projectile
                    projectile.remove_from_sprite_lists()

    def on_update(self, delta_time):
        if self.play_pause_button and self.play_pause_button.is_paused:
            return
        self.scene.update(delta_time)

        self.enemy_spawn_timer += delta_time

        # Spawn new enemies
        if self.enemy_spawn_timer > 1.0 and self.enemies_spawned < self.total_enemies_to_spawn:
            enemy = Enemy(self.spawn_point, self.enemy_path)
            self.scene["Enemies"].append(enemy)
            self.enemies_spawned += 1
            self.enemy_spawn_timer = 0.0

        # Update enemies individually to handle death animations
        for enemy in self.scene["Enemies"]:
            enemy.update(delta_time)

        # Remove dead enemies that finished their animation
        enemies_to_remove = []
        for enemy in self.scene["Enemies"]:
            if hasattr(enemy, 'should_remove') and enemy.should_remove():
                enemies_to_remove.append(enemy)
                # Give reward when enemy is completely removed
                self.money += enemy.reward
                print(f"Enemy killed! +{enemy.reward} gold")
        
        for enemy in enemies_to_remove:
            self.scene["Enemies"].remove(enemy)
        
        self.upgrade_menu.update()
    
        # Update towers and their attacks
        self.update_towers(delta_time)


if __name__ == "__main__":
    game = TowerDefense()
    arcade.run()