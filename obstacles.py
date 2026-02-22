import pygame

class Obstacle:
    def __init__(self, x, y, speed, obs_type):
        # Зберігаємо параметри у властивості об'єкта (self)
        self.x = x
        self.y = y
        self.speed = speed
        self.obs_type = obs_type

        # Створюємо прямокутник (rect) залежно від типу перешкоди
        if self.obs_type == "car":
            # Машина: ширина 50, висота 80
            self.rect = pygame.Rect(x, y, 50, 80)
        else:
            # Інше (наприклад, конус): ширина 30, висота 30
            self.rect = pygame.Rect(x, y, 30, 30)