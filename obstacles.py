import pygame
import random

class Obstacle:
  class Obstacle:
    def __init__(self, x, y, speed, obs_type):
        self.speed = speed
        self.obs_type = obs_type

        # Створюємо прямокутник
        if self.obs_type == "car":
            self.rect = pygame.Rect(x, y, 50, 80)
            # Спробуємо завантажити картинку, якщо її немає — залишиться колір
            try:
                self.image = pygame.image.load("assets/car_red.png")
                self.image = pygame.transform.scale(self.image, (50, 80))
            except:
                self.image = None
        else:
            self.rect = pygame.Rect(x, y, 30, 30)
            try:
                self.image = pygame.image.load("assets/cone.png")
                self.image = pygame.transform.scale(self.image, (30, 30))
            except:
                self.image = None

    def draw(self, surface):
        if self.image:
            # Малюємо картинку
            surface.blit(self.image, self.rect)
        else:
            # Резервний варіант (якщо файл картинки не знайдено)
            color = (200, 0, 0) if self.obs_type == "car" else (255, 165, 0)
            pygame.draw.rect(surface, color, self.rect)
            
    # Методи update та is_off_screen залишаються без змін

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
        self.game_time = 0       # Загальний час гри
        self.base_speed = 200     # Початкова швидкість для конусів (і база для машин)

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
            speed = self.base_speed + random.randint(150, 300)
        else:
            # Конуси просто "стоять", тому наближаються зі швидкістю дороги
            speed = self.base_speed
            
        # Створюємо об'єкт і додаємо в список
        new_obstacle = Obstacle(x, y, speed, obs_type)
        self.obstacles.append(new_obstacle)

    def update(self, dt, screen_height, screen_width):
        # 1. Накопичуємо час
        self.spawn_timer += dt
        self.game_time += dt
        
        # 2. Після 10 секунд починаємо поступово збільшувати швидкість руху перешкод (і, відповідно, складність гри)
        if self.game_time > 10:
            self.base_speed += 0.1  # Невеличке постійне прискорення кожного кадру після 10 сек
            self.base_speed = min(self.base_speed, 500)  # Обмежуємо максимальну швидкість

        # 3. Якщо пройшло більше 1.2 сек — створюємо нову перешкоду
        if self.spawn_timer >= 1.2:
            self.spawn(screen_width)
            self.spawn_timer = 0 # Скидаємо таймер
            
        # 4. Проходимо по кожній перешкоді (використовуємо зріз [:] для безпечного видалення)
        for obstacle in self.obstacles[:]:
            obstacle.update(dt) # Виклик методу руху самої перешкоди
            
            # 5. Якщо перешкода виїхала за екран — видаляємо її зі списку
            if obstacle.is_off_screen(screen_height):
                self.obstacles.remove(obstacle)

    def draw(self, surface):
        for obstacle in self.obstacles:
            obstacle.draw(surface)