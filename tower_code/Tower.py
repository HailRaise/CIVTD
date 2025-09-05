import arcade
import math

class Tower(arcade.Sprite):
    def __init__(self, tower_type: str, image_path: str, scale: float = 1.0):
        super().__init__(image_path, scale)
        
        # Tower properties based on type
        self.tower_type = tower_type
        self.properties = self._get_tower_properties()
        
        # Attack system
        self.attack_cooldown = 0.0
        self.current_target = None
        self.projectiles = arcade.SpriteList()
        
        # Level system
        self.level = 1
        self.max_level = 3
        self.upgrade_cost = self.properties["upgrade_cost"]
        
        # Visual effects
        self.attack_effect_timer = 0.0
        self.show_attack_effect = False
        self.attack_start_pos = (0, 0)
        self.attack_end_pos = (0, 0)

    def _get_tower_properties(self):
        """Return tower stats based on type"""
        base_stats = {
            "basic": {
                "range": 150,
                "damage": 15,
                "attack_speed": 1.0,  # attacks per second
                "cost": 100,
                "upgrade_cost": 50,
                "projectile_speed": 300,
                "description": "Basic tower with balanced stats"
            },
            "archer": {
                "range": 200,
                "damage": 10,
                "attack_speed": 1.5,
                "cost": 120,
                "upgrade_cost": 60,
                "projectile_speed": 400,
                "description": "Fast attacking archer tower"
            },
            "cannon": {
                "range": 120,
                "damage": 30,
                "attack_speed": 0.7,
                "cost": 150,
                "upgrade_cost": 75,
                "projectile_speed": 200,
                "description": "Slow but powerful cannon"
            },
            "sniper": {
                "range": 300,
                "damage": 25,
                "attack_speed": 0.5,
                "cost": 200,
                "upgrade_cost": 100,
                "projectile_speed": 500,
                "description": "Long range sniper tower"
            },
            "ice": {
                "range": 180,
                "damage": 5,
                "attack_speed": 0.8,
                "cost": 180,
                "upgrade_cost": 90,
                "projectile_speed": 250,
                "slow_effect": 0.5,  # 50% speed reduction
                "slow_duration": 3.0,
                "description": "Slows enemies"
            }
        }
        
        return base_stats.get(self.tower_type, base_stats["basic"])

    def update(self, delta_time: float):
        """Update tower state and attack cooldown"""
        self.attack_cooldown -= delta_time
        
        # Update projectiles
        self.projectiles.update()
        
        # Update attack effect timer
        if self.show_attack_effect:
            self.attack_effect_timer -= delta_time
            if self.attack_effect_timer <= 0:
                self.show_attack_effect = False

    def find_target(self, enemies: arcade.SpriteList):
        """Find the closest enemy within range"""
        self.current_target = None
        closest_distance = float('inf')
        
        for enemy in enemies:
            if not hasattr(enemy, 'alive') or not enemy.alive:
                continue
                
            distance = math.sqrt(
                (self.center_x - enemy.center_x) ** 2 +
                (self.center_y - enemy.center_y) ** 2
            )
            
            if distance <= self.properties["range"] and distance < closest_distance:
                self.current_target = enemy
                closest_distance = distance
        
        return self.current_target

    def attack(self, delta_time: float, enemies: arcade.SpriteList):
        """Attack if cooldown is ready and target is available"""
        if self.attack_cooldown > 0:
            return False
            
        target = self.find_target(enemies)
        if not target:
            return False
            
        # Create projectile or direct damage based on tower type
        if self.tower_type in ["basic", "archer", "cannon", "sniper"]:
            self.create_projectile(target)
        else:
            # Direct damage for special towers
            self.apply_direct_damage(target)
        
        # Reset cooldown
        self.attack_cooldown = 1.0 / self.properties["attack_speed"]
        
        # Show attack effect
        self.show_attack_effect = True
        self.attack_effect_timer = 0.2
        self.attack_start_pos = (self.center_x, self.center_y)
        self.attack_end_pos = (target.center_x, target.center_y)
        
        return True

    def create_projectile(self, target):
        """Create a projectile sprite"""
        projectile = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.5)
        projectile.center_x = self.center_x
        projectile.center_y = self.center_y
        projectile.properties = {
            "damage": self.properties["damage"],
            "speed": self.properties["projectile_speed"],
            "target": target,
            "tower_type": self.tower_type
        }
        self.projectiles.append(projectile)

    def apply_direct_damage(self, target):
        """Apply damage directly (for special towers)"""
        if hasattr(target, 'take_damage'):
            target.take_damage(self.properties["damage"])
            
            # Apply special effects
            if self.tower_type == "ice" and hasattr(target, 'apply_slow'):
                target.apply_slow(
                    self.properties["slow_effect"],
                    self.properties["slow_duration"]
                )

    def upgrade(self):
        """Upgrade the tower to next level"""
        if self.level >= self.max_level:
            return False
            
        self.level += 1
        
        # Improve stats with each level
        upgrade_multiplier = 1.2  # 20% improvement per level
        
        self.properties["damage"] = int(self.properties["damage"] * upgrade_multiplier)
        self.properties["range"] = int(self.properties["range"] * 1.1)
        self.properties["attack_speed"] *= 1.1
        self.properties["upgrade_cost"] = int(self.properties["upgrade_cost"] * 1.5)
        
        return True

    def draw_range(self):
        """Draw the tower's attack range"""
        arcade.draw_circle_outline(
            self.center_x,
            self.center_y,
            self.properties["range"],
            arcade.color.YELLOW,
            border_width=2
        )

    def draw_attack_effect(self):
        """Draw attack visual effect"""
        if self.show_attack_effect:
            # Draw laser/attack line
            arcade.draw_line(
                self.attack_start_pos[0],
                self.attack_start_pos[1],
                self.attack_end_pos[0],
                self.attack_end_pos[1],
                arcade.color.RED if self.tower_type == "cannon" else arcade.color.BLUE,
                3
            )

    def draw_info(self):
        """Draw tower information (for UI)"""
        info_text = [
            f"Type: {self.tower_type}",
            f"Level: {self.level}",
            f"Damage: {self.properties['damage']}",
            f"Range: {self.properties['range']}",
            f"Speed: {self.properties['attack_speed']:.1f}/s"
        ]
        
        for i, text in enumerate(info_text):
            arcade.draw_text(
                text,
                self.center_x - 60,
                self.center_y + 40 + i * 15,
                arcade.color.WHITE,
                10
            )

    def get_cost(self):
        """Get the cost of this tower type"""
        return self.properties["cost"]

    def can_afford_upgrade(self, money):
        """Check if player can afford upgrade"""
        return money >= self.properties["upgrade_cost"]