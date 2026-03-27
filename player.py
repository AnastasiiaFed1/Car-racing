import pygame

class PlayerCar():

    def __init__(self, x, y, speed : int):

        self.rect = pygame.Rect(x, y, 50, 100)
        self.speed = speed
        self.hitbox = self.rect.inflate(-10, -10)
        self.image = pygame.Surface((50, 100))
    
    def handle_input(self):

        left_bound = 0
        right_bound = 800
        upper_bound = 0
        bottom_bound = 600

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
            print(self.rect)
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
            print(self.rect)
        
        self.rect.x = max(left_bound, min(self.rect.x, right_bound - self.rect.width))

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            print(self.rect)
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            print(self.rect)

        self.rect.y = max(upper_bound, min(self.rect.y, bottom_bound - self.rect.height))
    
    def reset(self, start_x, start_y):
        
        self.rect.x = start_x
        self.rect.y = start_y
        
class Obstacle:
    def init(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)