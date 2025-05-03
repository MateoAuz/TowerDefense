import pygame
from collections import deque
from config import *

class BossCozy:
    def __init__(self, path):
        self.path_queue = deque(path)
        self.x, self.y = self.path_queue.popleft()
        self.target = self.path_queue.popleft() if self.path_queue else None
        self.speed = 1.5  # Slower speed for a boss
        self.health = 300
        self.max_health = 300

        # Load image
        self.image = pygame.image.load("images/boss.jpeg")
        self.image = pygame.transform.scale(self.image, (50, 50))

    def move(self):
        if not self.target:
            return True  # Reached end

        dx = self.target[0] - self.x
        dy = self.target[1] - self.y
        distance = (dx**2 + dy**2)**0.5

        if distance < self.speed:
            if self.path_queue:
                self.x, self.y = self.target
                self.target = self.path_queue.popleft()
            else:
                return True
        else:
            dir_x = dx / distance
            dir_y = dy / distance
            self.x += dir_x * self.speed
            self.y += dir_y * self.speed

        return False

    def draw(self, screen):
        screen.blit(self.image, (self.x - 25, self.y - 25))

        # Health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.x - 25, self.y - 35, 50, 5))
        green_width = int(50 * self.health / self.max_health)
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 25, self.y - 35, green_width, 5))

        # Label
        font = pygame.font.SysFont("arial", 14)
        label = font.render("BOSS", True, (255, 255, 255))
        screen.blit(label, (self.x - label.get_width() // 2, self.y - 50))
