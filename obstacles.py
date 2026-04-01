import pygame
import random

class Obstacle:
    def __init__(self, x, y, speed, obs_type):
        self.speed = speed
        self.obs_type = obs_type

        # Створюємо прямокутник
        if self.obs_type == "car":
            self.rect = pygame.Rect(x, y, 50, 80)
        else:
            self.rect = pygame.Rect(x, y, 30, 30)

    def draw(self, surface):
        if self.obs_type == "car":
            body = self.rect

            pygame.draw.rect(surface, (200, 40, 40), body, border_radius=10)

            window = pygame.Rect(body.x + 8, body.y + 10, body.w - 16, body.h // 4)
            pygame.draw.rect(surface, (210, 235, 255), window, border_radius=6)

            pygame.draw.rect(surface, (25, 25, 25), (body.x + 5, body.y + 14, 8, 16), border_radius=3)
            pygame.draw.rect(surface, (25, 25, 25), (body.right - 13, body.y + 14, 8, 16), border_radius=3)
            pygame.draw.rect(surface, (25, 25, 25), (body.x + 5, body.bottom - 30, 8, 16), border_radius=3)
            pygame.draw.rect(surface, (25, 25, 25), (body.right - 13, body.bottom - 30, 8, 16), border_radius=3)

        elif self.obs_type == "cone":
            body = self.rect

            # Трикутник
            points = [
                (body.centerx, body.top),
                (body.left, body.bottom - 4),
                (body.right, body.bottom - 4),
            ]
            pygame.draw.polygon(surface, (255, 140, 0), points)

            # Світла смуга
            stripe = [
                (body.centerx, body.top + 8),
                (body.left + 6, body.bottom - 14),
                (body.right - 6, body.bottom - 14),
            ]
            pygame.draw.polygon(surface, (255, 230, 180), stripe)

            # Основа
            base_rect = pygame.Rect(body.left - 2, body.bottom - 6, body.width + 4, 6)
            pygame.draw.rect(surface, (210, 210, 210), base_rect, border_radius=2)    

    def update(self, dt):
        self.rect.y += self.speed * dt # Оновлюємо позицію перешкоди, рухаючи її вниз по екрану зі швидкістю, залежною від часу (dt)

    def is_off_screen(self, screen_height):
        return self.rect.y > screen_height # Перевіряємо, чи перешкода вийшла за межі екрану (тобто, якщо її верхня межа (y) перевищує висоту екрану)
    
    def check_collision(self, player_rect):
        #Перевіряє, чи перешкода зіткнулася з гравцем
        return self.rect.colliderect(player_rect)

class Spawner:
    def __init__(self, road):
        self.obstacles = []
        self.spawn_timer = 0
        self.game_time = 0       # Загальний час гри
        self.base_speed = 200     # Початкова швидкість для конусів
        self.road = road

    def reset(self):
        self.obstacles = []
        self.spawn_timer = 0
        self.game_time = 0 
        self.base_speed = 200

    def spawn(self, screen_width):
      # 1. Визначаємо координати центрів смуг
        lane = random.randint(0, self.road.lane_count - 1)
        x = self.road.get_lane_center_x(lane) - 25
        y = -100
        
        obs_type = random.choice(["car", "cone"])
        
        # Використовуємо логіку швидкості з попереднього кроку
        if obs_type == "car":
            speed = self.base_speed + random.randint(150, 300)
        else:
            speed = self.base_speed
            
        new_obstacle = Obstacle(x, y, speed, obs_type)
        self.obstacles.append(new_obstacle)

    def update(self, dt, screen_height, screen_width):
        # 1. Накопичуємо час
        self.spawn_timer += dt
        self.game_time += dt
        removed_count = 0
        
        # 2. Після 10 секунд починаємо поступово збільшувати швидкість руху перешкод
        if self.game_time > 10:
            self.base_speed += 0.1  # Невеличке постійне прискорення кожного кадру після 10 сек
            self.base_speed = min(self.base_speed, 500)  # Обмежуємо максимальну швидкість

        # 3. Якщо пройшло більше 1.2 сек — створюємо нову перешкоду
        if self.spawn_timer >= 1.2:
            self.spawn(screen_width)
            self.spawn_timer = 0 # Скидаємо таймер
            
        # 4. Проходимо по кожній перешкоді 
        for obstacle in self.obstacles[:]:
            obstacle.update(dt) # Виклик методу руху самої перешкоди
            
            # 5. Якщо перешкода виїхала за екран — видаляємо її зі списку
            if obstacle.is_off_screen(screen_height):
                self.obstacles.remove(obstacle)
                removed_count += 1
        
        return removed_count

    def draw(self, surface):
        for obstacle in self.obstacles:
            obstacle.draw(surface)

    def check_all_collisions(self, player_rect):
        #Перевіряє зіткнення гравця з УСІМА активними перешкодами.
        #Повертає True, якщо сталася хоч одна аварія.
        for obstacle in self.obstacles:
            if obstacle.check_collision(player_rect):
                return True
        return False