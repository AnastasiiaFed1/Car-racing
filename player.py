import pygame

class PlayerCar():

    def __init__(self, x, y, speed : int):

        self.rect = pygame.Rect(x, y, 50, 100)
        self.speed = speed
        self.hitbox = self.rect.inflate(-10, -10)
        self.image = pygame.Surface((50, 100))
    
    def handle_input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
            print(self.rect)
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
            print(self.rect)
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            print(self.rect)
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            print(self.rect)

player = PlayerCar(100, 200, 5)
print(player.rect)  