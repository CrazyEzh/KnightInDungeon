import os

OBJECT_TEXTURE = os.path.join("texture", "objects")
ENEMY_TEXTURE = os.path.join("texture", "enemies")
ALLY_TEXTURE = os.path.join("texture", "ally")


class Settings:
    def __init__(self):
        self.base_stats = {
            "strength": 20,
            "endurance": 20,
            "intelligence": 5,
            "luck": 5
        }
