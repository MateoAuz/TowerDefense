import pygame
from collections import deque
from config import *


class BossCozy:
    def __init__(self, path):
        self.path_queue = deque(path)
        self.x, self.y = self.path_queue.popleft()
        self.target = self.path_queue.popleft() if self.path_queue else None
        self.speed = 20
        self.health = 300
        self.max_health = 100

        BOSS_SIZE = (60, 60)
        
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"images/boss_cozy/dark-f{i}.png").convert_alpha(),
                BOSS_SIZE
            )
            for i in range(1, 5)
        ]
        
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  

    def move(self):
        if not self.target:
            return True  

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

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        img = self.frames[self.current_frame]
        rect = img.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(img, rect)

        pygame.draw.rect(screen, (255, 0, 0), (self.x - 25, self.y - 35, 50, 5))
        green_width = int(50 * self.health / self.max_health)
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 25, self.y - 35, green_width, 5))

        font = pygame.font.SysFont("arial", 14)
        label = font.render("BOSS", True, (255, 255, 255))
        screen.blit(label, (self.x - label.get_width() // 2, self.y - 50))
