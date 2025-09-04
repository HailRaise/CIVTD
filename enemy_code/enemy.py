import arcade

class Enemy(arcade.TextureAnimationSprite):
    def __init__(self, spawn_point, path, speed=2):
        super().__init__(scale=2.0)
        self.center_x, self.center_y = spawn_point
        self.path = path
        self.path_index = 0
        self.speed = speed

        sprite_sheet_path = "assets/enemies/Skeleton Walk.png"
        frame_width = 22
        frame_height = 33
        num_frames = 13

        # Instead of TextureKeyframe, use .append_texture() directly
        for i in range(num_frames):
            tex = arcade.load_texture(
                sprite_sheet_path,
                x=i * frame_width,
                y=0,
                width=frame_width,
                height=frame_height
            )
            self.append_texture(tex)

        self.set_texture(0)

        if self.path and self.path[0] == spawn_point:
            self.path_index = 1

        self.current_frame = 0
        self.time_accumulator = 0

    def update(self, delta_time: float = 1 / 60):
        # Manual animation loop
        self.time_accumulator += delta_time
        if self.time_accumulator > 0.1:  # 100ms per frame
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            self.set_texture(self.current_frame)
            self.time_accumulator = 0

        # Movement logic
        if self.path_index >= len(self.path):
            return

        dest_x, dest_y = self.path[self.path_index]
        dx = dest_x - self.center_x
        dy = dest_y - self.center_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:
            step = min(self.speed, distance)
            self.center_x += dx / distance * step
            self.center_y += dy / distance * step

        if distance < self.speed:
            self.path_index += 1
