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
    
    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Obstacle():
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Car Racing")

player = PlayerCar(100, 200, 5)

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.handle_input()

    obstacle1 = Obstacle(200, 250, 50, 50)
    obstacle2 = Obstacle(400, 200, 50, 50)

    pygame.draw.rect(screen, (0, 255, 0), obstacle1.rect)
    pygame.draw.rect(screen, (0, 0, 255), obstacle2.rect)

    if player.check_collision([obstacle1, obstacle2]):
        player.reset(100,200)

    player.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()