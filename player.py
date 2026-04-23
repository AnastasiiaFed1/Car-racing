import pygame


class PlayerCar():

    def __init__(self, x, y, speed: int):

        self.rect = pygame.Rect(x, y, 50, 100)
        self.speed = speed

    def handle_input(self, left_bound, right_bound):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10

        self.rect.x = max(left_bound, min(self.rect.x, right_bound - self.rect.width))

    def reset(self, start_x, start_y):

        self.rect.x = start_x
        self.rect.y = start_y

    def draw(self, screen):
        body = self.rect

        pygame.draw.rect(screen, (70, 130, 255), body, border_radius=10)

        window = pygame.Rect(body.x + 10, body.y + 12, body.w - 20, body.h // 4)
        pygame.draw.rect(screen, (210, 235, 255), window, border_radius=6)

        pygame.draw.rect(screen, (25, 25, 25), (body.x + 7, body.y + 16, 8, 18), border_radius=3)
        pygame.draw.rect(screen, (25, 25, 25), (body.right - 15, body.y + 16, 8, 18), border_radius=3)
        pygame.draw.rect(screen, (25, 25, 25), (body.x + 7, body.bottom - 34, 8, 18), border_radius=3)
        pygame.draw.rect(screen, (25, 25, 25), (body.right - 15, body.bottom - 34, 8, 18), border_radius=3)

        pygame.draw.rect(screen, (255, 255, 255), body, 2, border_radius=10)
