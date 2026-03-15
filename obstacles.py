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
    
    def draw(self, surface):
        if self.obs_type == "car":
            color = (200, 0, 0)  # Червоний для машин
        else:
            color = (255, 165, 0)  # Помаранчевий для конусів
            
        pygame.draw.rect(surface, color, self.rect)
    

class Spawner:
    def __init__(self):
        self.obstacles = []
        self.spawn_timer = 0

    def spawn(self, screen_width):
        #Створює одну перешкоду у випадковому місці по горизонталі, з випадковим типом та швидкістю
        # Випадкова позиція по горизонталі
        x = random.randint(100, screen_width - 100)
        y = -100 
        
        # Випадковий вибір типу перешкоди
        obs_type = random.choice(["car", "cone"])
        
        # Визначаємо швидкість руху об'єкта відносно гравця
        if obs_type == "car":
            # Машини їдуть швидше
            speed = random.randint(350, 500)
        else:
            # Конуси просто "стоять", тому наближаються зі швидкістю дороги
            speed = 200 
            
        # Створюємо об'єкт і додаємо в список
        new_obstacle = Obstacle(x, y, speed, obs_type)
        self.obstacles.append(new_obstacle)

    def update(self, dt, screen_height, screen_width):
        # 1. Накопичуємо час
        self.spawn_timer += dt
        
        # 2. Якщо пройшло більше 1.2 сек — створюємо нову перешкоду
        if self.spawn_timer >= 1.2:
            self.spawn(screen_width)
            self.spawn_timer = 0 # Скидаємо таймер
            
        # 3. Проходимо по кожній перешкоді (використовуємо зріз [:] для безпечного видалення)
        for obstacle in self.obstacles[:]:
            obstacle.update(dt) # Викликаємо метод руху самої перешкоди
            
            # 4. Якщо перешкода виїхала за екран — видаляємо її зі списку
            if obstacle.is_off_screen(screen_height):
                self.obstacles.remove(obstacle)

    def draw(self, surface):
        for obstacle in self.obstacles:
            obstacle.draw(surface)