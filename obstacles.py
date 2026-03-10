import pygame
import random

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
            # Інше (конус): ширина 30, висота 30
            self.rect = pygame.Rect(x, y, 30, 30)

    def update(self, dt):
        self.rect.y += self.speed * dt # Оновлюємо позицію перешкоди, рухаючи її вниз по екрану зі швидкістю, залежною від часу (dt)

    def is_off_screen(self, screen_height):
        return self.rect.y > screen_height # Перевіряємо, чи перешкода вийшла за межі екрану (тобто, якщо її верхня межа (y) перевищує висоту екрану)
    
class Spawner:
    def __init__(self):
        self.obstacles = []
        self.spawn_timer = 0

    def spawn(self, screen_width):
        #Створює одну перешкоду у випадковому місці
        x = random.randint(100, screen_width - 100)
        y = -100
        speed = 250  # Поки що фіксована швидкість
        new_obs = Obstacle(x, y, speed, "car")
        self.obstacles.append(new_obs)