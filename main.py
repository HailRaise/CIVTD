import arcade
from core.map_loader import load_map_and_path
from enemy_code.enemy import Enemy
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
        self.tile_map, self.scene, self.spawn_point, self.enemy_path = load_map_and_path(MAP_PATH, TILE_SCALING)

        # --- Set up enemy list ---
        self.scene.add_sprite_list("Enemies", use_spatial_hash=True)
        self.enemy_spawn_timer = 0.0
        self.enemies_spawned = 0
        self.total_enemies_to_spawn = 15

    def on_draw(self):
        self.clear()
        self.scene.draw()

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

if __name__ == "__main__":
    game = TowerDefense()
    game.setup()
    arcade.run()
