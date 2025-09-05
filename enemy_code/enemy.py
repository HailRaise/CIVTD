import arcade
import math

class Enemy(arcade.TextureAnimationSprite):
    def __init__(self, spawn_point, path, speed=2, health=100, reward=25):
        super().__init__(scale=2.0)
        self.center_x, self.center_y = spawn_point
        self.path = path
        self.path_index = 0
        self.speed = speed
        self.health = health
        self.max_health = health
        self.reward = reward
        self.alive = True
        self.reached_end = False

        # Load walk animation
        sprite_sheet_path = "assets/enemies/Skeleton/Sprite Sheets/Skeleton Walk.png"
        frame_width = 22
        frame_height = 33
        num_frames = 13

        sheet = arcade.load_spritesheet(sprite_sheet_path)
        textures = sheet.get_texture_grid(
            size=(22, 33),
            columns=13,
            count=13,
        )

        # Add walk frames
        for tex in textures:
            self.append_texture(tex)
        
        # Load death animation (you'll need to create this spritesheet)
        death_sheet_path = "assets/enemies/Skeleton/Sprite Sheets/Skeleton Death.png"
        try:
            death_sheet = arcade.load_spritesheet(death_sheet_path)
            death_textures = death_sheet.get_texture_grid(
                size=(22, 33),  # Adjust based on your death animation frame size
                columns=8,      # Adjust based on your death animation frames
                count=8,
            )
            self.death_textures = death_textures
        except:
            # Fallback: use a single frame or create simple death effect
            self.death_textures = None

        self.set_texture(0)

        # Skip the first path point if it equals the spawn
        if self.path and self.path[0] == (self.center_x, self.center_y):
            self.path_index = 1

        # Animation control
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.seconds_per_frame = 0.1

        # Death animation control
        self.is_dying = False
        self.death_animation_time = 0.0
        self.death_animation_duration = 1.0  # seconds for death animation
        self.death_frame = 0

        # HP bar dimensions
        self.hp_bar_width = 40
        self.hp_bar_height = 5
        self.hp_bar_offset = 25

    def take_damage(self, damage):
        """Reduce enemy health by damage amount"""
        if self.is_dying:
            return False  # Already dying
            
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.start_death_animation()
            return True  # Enemy died
        return False  # Enemy still alive

    def start_death_animation(self):
        """Start the death animation sequence"""
        self.alive = False
        self.is_dying = True
        self.death_animation_time = 0.0
        self.death_frame = 0
        
        # If we have death textures, use them
        if self.death_textures:
            self.textures = self.death_textures
            self.set_texture(0)

    def update(self, delta_time: float = 1/60):
        if self.is_dying:
            # Handle death animation
            self.update_death_animation(delta_time)
            return
            
        if not self.alive:
            return
            
        # Normal walk animation
        self.time_accumulator += delta_time
        if self.time_accumulator >= self.seconds_per_frame:
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            self.set_texture(self.current_frame)
            self.time_accumulator = 0.0

        # Movement
        if self.path_index >= len(self.path):
            self.reached_end = True
            return

        dest_x, dest_y = self.path[self.path_index]
        dx = dest_x - self.center_x
        dy = dest_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            step = min(self.speed, distance)
            self.center_x += dx / distance * step
            self.center_y += dy / distance * step

        if distance < self.speed:
            self.path_index += 1

    def update_death_animation(self, delta_time):
        """Update the death animation"""
        self.death_animation_time += delta_time
        
        if self.death_textures:
            # Animate through death frames
            frame_time = self.death_animation_duration / len(self.death_textures)
            current_frame = int(self.death_animation_time / frame_time)
            
            if current_frame < len(self.death_textures):
                self.set_texture(current_frame)
            else:
                # Animation complete, mark for removal
                self.is_dying = False
        else:
            # Simple fade-out effect if no death animation
            self.alpha = int(255 * (1 - self.death_animation_time / self.death_animation_duration))
            if self.death_animation_time >= self.death_animation_duration:
                self.is_dying = False

    def draw_hp_bar(self):
        """Draw the HP bar above the enemy"""
        if not self.alive or self.is_dying:
            return
            
        # Calculate HP percentage
        hp_percentage = max(0, self.health / self.max_health)
        
        # Background bar (gray)
        arcade.draw_lbwh_rectangle_filled(
            self.center_x,
            self.center_y + self.hp_bar_offset,
            self.hp_bar_width,
            self.hp_bar_height,
            arcade.color.GRAY
        )
        
        # Health bar (green, red when low)
        if hp_percentage > 0.3:
            bar_color = arcade.color.GREEN
        else:
            bar_color = arcade.color.RED
            
        arcade.draw_lbwh_rectangle_filled(
            self.center_x - (self.hp_bar_width * (1 - hp_percentage)) / 2,
            self.center_y + self.hp_bar_offset,
            self.hp_bar_width * hp_percentage,
            self.hp_bar_height,
            bar_color
        )

    def should_remove(self):
        """Check if enemy should be removed from game"""
        return not self.alive and not self.is_dying

    def draw(self):
        """Override draw to include HP bar"""
        if self.is_dying or self.alive:
            if self.alive:  # Only draw HP bar if alive
                self.draw_hp_bar()