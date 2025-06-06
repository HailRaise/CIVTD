import arcade
from core.map_loader import load_map_and_path
from core.enemy_spawner import spawn_enemy

SCREEN_WIDTH = 1200
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
        self.tile_map, self.scene, spawn_point, enemy_path = load_map_and_path(MAP_PATH, TILE_SCALING)
        

        # --- Spawn enemy ---
        self.enemy = spawn_enemy(spawn_point, enemy_path)

        # Add enemy to the scene instead of a separate list
        self.scene.add_sprite_list("Enemies", use_spatial_hash=True)

        self.scene["Enemies"].append(self.enemy)
        print(f"[DEBUG] Scene['Enemies'] length: {len(self.scene['Enemies'])}")
        print(f"[DEBUG] Scene['Enemies'] type: {type(self.scene['Enemies'][0])}")



    def on_draw(self):
        self.clear()
        self.scene.draw()
       
            


        # Optional: draw the path for debugging
        for x, y in self.enemy.path:
            arcade.draw_circle_filled(x, y, 5, arcade.color.RED)

    def on_update(self, delta_time):
        print("[DEBUG] Window.update() called")
        self.scene.update(delta_time)
        for sprite in self.scene["Enemies"]:
            sprite.update(delta_time)

if __name__ == "__main__":
    game = TowerDefense()
    game.setup()
    arcade.run()
