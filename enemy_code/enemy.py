import arcade

class Enemy(arcade.Sprite):
    def __init__(self, spawn_point, path, speed=2):
        super().__init__(":resources:images/enemies/slimeBlock.png", scale=0.5)  # Use this texture for now to be sure
        self.center_x, self.center_y = spawn_point
        self.path = path
        self.path_index = 0
        self.speed = speed

        print(f"[DEBUG] Spawn at {spawn_point}")
        print(f"[DEBUG] Full path: {self.path}")

        # Fix: skip first point if it's the same as spawn
        if self.path and self.path[0] == spawn_point:
            self.path_index = 1

    def update(self, delta_time: float = 1/60):
        print("[DEBUG] Enemy.update() called")

        if self.path_index >= len(self.path):
            print("[DEBUG] Enemy finished path.")
            return

        dest_x, dest_y = self.path[self.path_index]
        print(f"[DEBUG] From: ({self.center_x:.2f}, {self.center_y:.2f}) → To: ({dest_x:.2f}, {dest_y:.2f})")

        dx = dest_x - self.center_x
        dy = dest_y - self.center_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:
            step = min(self.speed, distance)
            self.center_x += dx / distance * step
            self.center_y += dy / distance * step
            print(f"[DEBUG] Moved to: ({self.center_x:.2f}, {self.center_y:.2f})")

        if distance < self.speed:
            print(f"[DEBUG] Reached waypoint {self.path_index}")
            self.path_index += 1
