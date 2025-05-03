import pygame

class Cozy:
    def __init__(self, path):
        self.path = path
        self.index = 0
        self.x, self.y = path[0]
        self.speed = 1
        self.health = 100

        # Cargar frames de animación
        self.frames = [
            pygame.image.load(f"images/cozy_robot/frame_{i}.png").convert_alpha()
            for i in range(3)  # Número de frames
        ]
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # velocidad del cambio de frame

    def move(self):
        if self.index < len(self.path) - 1:
            tx, ty = self.path[self.index + 1]
            dx = tx - self.x
            dy = ty - self.y
            dist = (dx**2 + dy**2)**0.5
            if dist != 0:
                dx /= dist
                dy /= dist

            self.x += dx * self.speed
            self.y += dy * self.speed

            if dist < 2:
                self.index += 1
            return False
        return True

    def draw(self, screen):
        # Animar
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        img = self.frames[self.current_frame]
        rect = img.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(img, rect)
