from core.LevelData import LevelData

class LevelManager():
    def __init__(self):
        self.levels = {
            1: LevelData(
                "assets/maps/first_round_map_obj.tmx",
                waves= [
                    {"enemy": "grunt", "count": 10, "spawn_rate": 1.0},
                    {"enemy": "fast", "count": 5, "spawn_rate": 0.7}
                ],
                money_start= 1000,
                lives= 10
            ), 
            2: LevelData(
                "assets\maps\second_round_map.tmx",
                waves=[
                    {"enemy": "grunt", "count": 15, "spawn_rate": 0.9},
                    {"enemy": "tank", "count": 3, "spawn_rate": 2.0}
                ],
                money_start=1200,
                lives=15
            )


        }
        self.current_level = 1

    def get_current(self):
        return self.levels[self.current_level]

    def next_level(self):
        if self.current_level + 1 in self.levels:
            self.current_level += 1
            return True
        return False