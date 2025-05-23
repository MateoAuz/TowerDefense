from cozy import Cozy
from boss_cozy import BossCozy

WIDTH, HEIGHT = 800, 600
FPS = 60

BG_COLOR = (30, 30, 30)
COZY_COLOR = (200, 50, 50)
TOWER_COLOR = (50, 150, 255)
PROJECTILE_COLOR = (0, 0, 0)


COZY_TYPES = [
    {"class": Cozy, "from_wave": 1, "to_wave": 4},
    {"class": BossCozy, "from_wave": 5, "to_wave": 5}
]


WAVES = [
    {"cozy": 5},
    {"cozy": 7},
    {"cozy": 10},
    {"cozy": 12},
    {"cozy": 10, "boss": 1}
]


path = [
    (0, 100),
    (200, 100),
    (200, 300),
    (600, 300),
    (600, 500),
    (800, 500)
]

TOWER_TYPES = {
    "basic": {
        "color": (50, 150, 255),  
        "damage": 15,
        "range": 150,
        "cooldown": 60,
        "cost": 50,
        "image": "images/towers/torreBase.png"
    },
    "sniper": {
        "color": (100, 255, 100),  
        "damage": 50,
        "range": 250,
        "cooldown": 90,
        "cost": 100,
        "image": "images/towers/torreMedia.png"
    },
    "rapid": {
        "color": (255, 100, 100),  
        "damage": 5,
        "range": 120,
        "cooldown": 15,
        "cost": 60,
        "image": "images/towers/torreRapida.png"
    }
}


TOWER_LIST = ["basic", "sniper", "rapid"]


