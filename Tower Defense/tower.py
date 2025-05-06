import pygame
from config import *
from projectile import Projectile
from config import *

class Tower:
    def __init__(self, x, y, tipo="basic"):
        self.x = x
        self.y = y
        self.tipo = tipo
        stats = TOWER_TYPES[tipo]
        self.color = stats["color"]
        self.range = stats["range"]
        self.cooldown = stats["cooldown"]
        self.damage = stats["damage"]
        self.counter = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 20)
        def draw(self, screen):
            pygame.draw.circle(screen, self.color, (self.x, self.y), 20)


    def shoot(self, enemies, projectiles):
        if self.counter > 0:
            self.counter -= 1
            return
        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = (dx**2 + dy**2)**0.5
            if distance <= self.range:
                projectiles.append(Projectile(self.x, self.y, enemy, self.damage))
                self.counter = self.cooldown
                break

