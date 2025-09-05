import arcade

class Enemy(arcade.TextureAnimationSprite):
    def __init__(self, spawn_point, path, speed=2):
        super().__init__(scale=2.0)
        self.center_x, self.center_y = spawn_point
        self.path = path
        self.path_index = 0
        self.speed = speed

        sprite_sheet_path = "assets\enemies\Skeleton\Sprite Sheets\Skeleton Walk.png"
        frame_width = 22
        frame_height = 33
        num_frames = 13


        sheet = arcade.load_spritesheet(sprite_sheet_path)
        textures = sheet.get_texture_grid(
               size=(22, 33),   # each frame’s width/height
                columns=13,      # how many frames per row
                count=13,        # total number of frames
        )
        # print(f"[DEBUG] Loaded {len(textures)} frames")
        # print(f"[DEBUG] Frame size: {textures[0].width}x{textures[0].height}")
        # textures[0].image.show() 

         # Add each frame to the sprite
        for tex in textures:
            self.append_texture(tex)
        
        self.set_texture(0)

        # Skip the first path point if it equals the spawn
        if self.path and self.path[0] == (self.center_x, self.center_y):
            self.path_index = 1

        # ---- Animation control ----
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.seconds_per_frame = 0.1  # 100 ms

    def update(self, delta_time: float = 1/60):
        # ----- Animation -----
            self.time_accumulator += delta_time
            if self.time_accumulator >= self.seconds_per_frame:
                self.current_frame = (self.current_frame + 1) % len(self.textures)
                self.set_texture(self.current_frame)
                self.time_accumulator = 0.0

            # ----- Movement -----
            if self.path_index >= len(self.path):
                return

            dest_x, dest_y = self.path[self.path_index]
            dx = dest_x - self.center_x
            dy = dest_y - self.center_y
            distance = (dx * dx + dy * dy) ** 0.5

            if distance > 0:
                step = min(self.speed, distance)
                self.center_x += dx / distance * step
                self.center_y += dy / distance * step

            if distance < self.speed:
                self.path_index += 1

        
