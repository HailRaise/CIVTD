import arcade
from core.map_loader import load_map_and_path
from enemy_code.enemy import Enemy
from core.enemy_spawner import spawn_enemy
from tower_code.TowerMenu import TowerMenuClass   
from tower_code.Tower import Tower
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
        self.money = 10000  # Add money system

    def setup(self):
        # --- Load map and scene, extract spawn and path ---
        self.tile_map, self.scene, self.spawn_point, self.enemy_path = load_map_and_path(MAP_PATH, TILE_SCALING)

        # --- Set up enemy list ---
        self.scene.add_sprite_list("Enemies", use_spatial_hash=True)
        self.enemy_spawn_timer = 0.0
        self.enemies_spawned = 0
        self.total_enemies_to_spawn = 15
        self.active_tower = None

        # Setup towers
        self.tower_menu = TowerMenuClass(UI_BAR_HEIGHT)
        self.scene.add_sprite_list("Towers")
        self.tower_menu.add_icon("assets/free-archer-towers-pixel-art-for-tower-defense/1 Upgrade/first_build.png", 60, "basic")
        
        # Add ghost tower variables
        self.ghost_tower = None
        self.selected_tower_type = None
        self.selected_tower_image = None
        self.selected_tower_scale = None

    def on_draw(self):
        self.clear()
        self.scene.draw()
        
        # Draw enemies (they handle their own drawing including death animations)
        for enemy in self.scene["Enemies"]:
            enemy.draw()
        
        # Draw towers
        self.scene["Towers"].draw()
        
        # Draw tower projectiles and attack effects
        for tower in self.scene["Towers"]:
            tower.projectiles.draw()
            tower.draw_attack_effect()
        
        # Draw ghost tower if it exists
        if self.ghost_tower:
            arcade.draw_sprite(self.ghost_tower)
        
        # Draw range for selected tower
        if self.active_tower is not None:
            arcade.draw_circle_outline(
                self.active_tower.center_x,
                self.active_tower.center_y,
                self.active_tower.properties.get("range", TOWER_RANGE),
                arcade.color.YELLOW,
                border_width=3
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

    def on_update(self, delta_time):
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
    
        # Update towers and their attacks
        self.update_towers(delta_time)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """Update ghost tower position to follow mouse"""
        if self.ghost_tower and y > UI_BAR_HEIGHT:
            self.ghost_tower.center_x = x
            self.ghost_tower.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        # First, check if the user clicked the menu
        tower_clicked = arcade.get_sprites_at_point((x, y), self.tower_menu.icons)
        if tower_clicked:
            clicked_icon = tower_clicked[-1]
            
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
            
            print(f"Selected tower: {self.selected_tower_type} at ({x}, {y})")
            self.active_tower = None  
            return

        # Check if clicking on an existing tower to select it
        existing_tower_clicked = arcade.get_sprites_at_point((x, y), self.scene["Towers"])
        if existing_tower_clicked:
            self.active_tower = existing_tower_clicked[-1]
            print(f"Selected tower: {self.active_tower.tower_type} (Level {self.active_tower.level})")
            return

        # If we have a ghost tower (tower selected) and click is ABOVE the UI bar
        if self.ghost_tower and y > UI_BAR_HEIGHT:
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
            self.tower_menu.selected_tower_type = None

    def on_key_press(self, key, modifiers):
        """Handle key presses - ESC to cancel tower placement"""
        if key == arcade.key.ESCAPE:
            # Cancel tower placement
            self.ghost_tower = None
            self.selected_tower_type = None
            if hasattr(self.tower_menu, 'selected_tower_type'):
                self.tower_menu.selected_tower_type = None
            print("Tower placement cancelled")

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

if __name__ == "__main__":
    game = TowerDefense()
    game.setup()
    arcade.run()