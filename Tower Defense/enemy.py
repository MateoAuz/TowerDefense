import pygame
from config import COZY_COLOR

class Enemy:
    def __init__(self, path):
        self.path = path
        self.current_point = 0
        self.x, self.y = self.path[0]
        self.speed = 2
        self.health = 100  # 💓 nueva vida
        
    def move(self):
        if self.current_point + 1 >= len(self.path):
            return  True # Fin del camino

        target_x, target_y = self.path[self.current_point + 1]
        dx, dy = target_x - self.x, target_y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.speed:
            self.current_point += 1
        else:
            direction_x = dx / distance
            direction_y = dy / distance
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed
        return False
        
    def draw(self, screen):
        # Círculo del enemigo
        pygame.draw.circle(screen, COZY_COLOR, (int(self.x), int(self.y)), 15)

        # Barra de vida
        pygame.draw.rect(screen, (255, 0, 0), (self.x - 15, self.y - 20, 30, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 15, self.y - 20, 30 * self.health / 100, 5))
