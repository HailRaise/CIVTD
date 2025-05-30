import arcade

class Enemy(arcade.Sprite):
    def __init__(self, spawn_point, path, speed=2):
        super().__init__("assets/enemies/warrior.png", scale=0.1)
        self.path = path
        self.path_index = 0
        self.speed = speed

        # Spawn enemy at the given spawn point
        self.center_x, self.center_y = spawn_point
        print(f"[DEBUG] Spawn enemy at: {self.center_x}, {self.center_y}")
        print(f"[DEBUG] Path to follow: {self.path}")

    def update(self):
        if self.path_index >= len(self.path):
            print("[DEBUG] Enemy reached end of path.")
            return

        dest_x, dest_y = self.path[self.path_index]
        print(f"[DEBUG] Enemy at ({self.center_x:.2f}, {self.center_y:.2f}), moving towards ({dest_x}, {dest_y})")

        self.center_x, self.center_y = arcade.move_towards_point(
            (self.center_x, self.center_y),
            (dest_x, dest_y),
            self.speed
        )

        # If close enough, move to next path index
        if arcade.get_distance_between_sprites(self, arcade.Sprite(center_x=dest_x, center_y=dest_y)) < self.speed:
            print(f"[DEBUG] Enemy reached point {self.path_index}: ({dest_x}, {dest_y})")
            self.path_index += 1
