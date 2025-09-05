import arcade
from core.map_loader import load_map_and_path
from enemy_code.enemy import Enemy
from core.enemy_spawner import spawn_enemy
from tower_code.TowerMenu import TowerMenuClass   
SCREEN_WIDTH = 1200
UI_BAR_HEIGHT = 150
SCREEN_HEIGHT = 950
SCREEN_TITLE = "Tower Defense Starter"
TILE_SCALING = 1.0
MAP_PATH = "assets/maps/first_round_map_obj.tmx"

class TowerDefense(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # --- Load map and scene, extract spawn and path ---
        self.tile_map, self.scene, self.spawn_point, self.enemy_path = load_map_and_path(MAP_PATH, TILE_SCALING)

        # --- Set up enemy list ---
        self.scene.add_sprite_list("Enemies", use_spatial_hash=True)
        self.enemy_spawn_timer = 0.0
        self.enemies_spawned = 0
        self.total_enemies_to_spawn = 15

        #setup towers
        self.tower_menu = TowerMenuClass(UI_BAR_HEIGHT)
        self.scene.add_sprite_list("Towers")
        self.tower_menu.add_icon("assets/free-archer-towers-pixel-art-for-tower-defense/1 Upgrade/first_build.png", 60, "basic")
        #self.tower_menu.add_icon("assets/towers/sniper_tower.png", 160, "sniper")
    

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.scene["Enemies"].draw()
        self.scene["Towers"].draw()
        arcade.draw_lbwh_rectangle_filled(
        0,                # left
        0,                # bottom
        SCREEN_WIDTH,     # width
        UI_BAR_HEIGHT,    # height
        arcade.color.DARK_SLATE_GRAY
    )
        self.tower_menu.draw()


        # Optional: draw the path
        for x, y in self.enemy_path:
            arcade.draw_circle_filled(x, y, 5, arcade.color.RED)

    def on_update(self, delta_time):
        self.scene.update(delta_time)

        self.enemy_spawn_timer += delta_time

        if self.enemy_spawn_timer > 1.0 and self.enemies_spawned < self.total_enemies_to_spawn:
            enemy = Enemy(self.spawn_point, self.enemy_path)
            self.scene["Enemies"].append(enemy)
            self.enemies_spawned += 1
            self.enemy_spawn_timer = 0.0

        self.scene["Enemies"].update()

    def on_mouse_press(self, x, y, button, modifiers):
        # First, check if the user clicked the menu
        tower_type = self.tower_menu.handle_click(x, y)
        if tower_type:
            # User clicked an icon, select it and return
            return

        # If a tower is already selected and the click is ABOVE the UI bar
        if self.tower_menu.selected_tower_type and y > UI_BAR_HEIGHT:
            new_tower = arcade.Sprite(
            self.tower_menu.selected_tower_image,
            self.tower_menu.selected_tower_scale
        )
        new_tower.center_x = x
        new_tower.center_y = y
        self.scene["Towers"].append(new_tower)

        print(f"Placed tower: {self.tower_menu.selected_tower_type}")
        self.tower_menu.selected_tower_type = None


if __name__ == "__main__":
    game = TowerDefense()
    game.setup()
    arcade.run()
