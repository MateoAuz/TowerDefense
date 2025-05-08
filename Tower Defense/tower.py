import pygame
from config import *
from projectile import Projectile
from config import *

import pygame

class Tower:
    def __init__(self, x, y, tipo="basic"):
        self.x = x
        self.y = y
        self.tipo = tipo
        stats = TOWER_TYPES[tipo]
        self.range = stats["range"]
        self.cooldown = stats["cooldown"]
        self.damage = stats["damage"]
        self.counter = 0

        self.image = pygame.image.load(stats["image"])
        self.image = pygame.transform.scale(self.image, (40, 40))

    def draw(self, screen):
        screen.blit(self.image, (self.x - 20, self.y - 20))  


    def shoot(self, cozies, projectiles):
        if self.counter > 0:
            self.counter -= 1
            return
        for cozy in cozies:
            dx = cozy.x - self.x
            dy = cozy.y - self.y
            distance = (dx**2 + dy**2)**0.5
            if distance <= self.range:
                projectiles.append(Projectile(self.x, self.y, cozy, self.damage))
                self.counter = self.cooldown
                break

