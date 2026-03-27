import pygame

class PlayerCar():

    def __init__(self, x, y, speed : int):

        self.rect = pygame.Rect(x, y, 50, 100)
        self.speed = speed
        self.hitbox = self.rect.inflate(-10, -10)
        self.image = pygame.Surface((50, 100))

player = PlayerCar(100, 200, 5)
print(player.rect)  