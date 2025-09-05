import arcade

class TowerMenuClass:
    def __init__(self, height):
        self.height = height
        self.icons = arcade.SpriteList()

        # Selected tower info
        self.selected_tower_type = None
        self.selected_tower_image = None
        self.selected_tower_scale = None

    def add_icon(self, image_path: str, x: int, tower_type: str, scale: float = 0.2):
        """Add a tower icon to the menu bar"""
        icon = arcade.Sprite(image_path, scale)
        icon.center_x = x
        icon.center_y = self.height // 2
        icon.properties = {
            "type": tower_type,
            "image_path": image_path,
            "scale": scale
        }
        self.icons.append(icon)

    def draw(self):
        self.icons.draw()

    def handle_click(self, x: int, y: int):
        """Check if a tower icon was clicked"""
        tower_clicked = arcade.get_sprites_at_point((x, y), self.icons, )
        if tower_clicked:
            clicked_icon = tower_clicked[-1]   # take topmost if overlap
            
            self.selected_tower_type = clicked_icon.properties["type"]
            self.selected_tower_image = clicked_icon.properties["image_path"]
            self.selected_tower_scale = clicked_icon.properties["scale"]
            print(f"Selected tower: {self.selected_tower_type}")
            self.ghost_tower = arcade.Sprite(
            self.selected_tower_image, 
            self.selected_tower_scale
        )
            self.ghost_tower.alpha = 128
            self.ghost_tower.center_x = x
            self.ghost_tower.center_y = y
            return self.selected_tower_type
        return None
