import pygame
from config import *

class Projectile:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.damage = damage

    def move(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance < self.speed or distance == 0:
            self.target.health -= self.damage
            return True
        dir_x = dx / distance
        dir_y = dy / distance
        self.x += dir_x * self.speed
        self.y += dir_y * self.speed
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, PROJECTILE_COLOR, (int(self.x), int(self.y)), 5)
