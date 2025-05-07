import pygame
from collections import deque

class Cozy:
    def __init__(self, path):
        self.path_queue = deque(path)
        self.x, self.y = self.path_queue.popleft()
        self.target = self.path_queue.popleft() if self.path_queue else None
        self.speed = 1
        self.health = 100
        self.max_health = 100

        # Cargar frames de animación
        self.frames = [
            pygame.image.load(f"images/cozy_robot/frame_{i}.png").convert_alpha()
            for i in range(3)
        ]
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # Velocidad del cambio de frame

    def move(self):
        if not self.target:
            return True  # Llegó al final del camino

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
        # Animar
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        img = self.frames[self.current_frame]
        rect = img.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(img, rect)

        
