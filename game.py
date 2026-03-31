import pygame

from settings import SCREEN_W, SCREEN_H, FPS, BG_COLOR, TEXT_COLOR
from state import GameState

from player import PlayerCar
from obstacles import ObstacleManager
from road import Road
from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Racing")

        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)

        self.state = GameState.MENU
        self.score = 0
        self.time_score = 0.0

        self.road = Road()
        self.player = PlayerCar()
        self.obstacles = ObstacleManager()
        self.ui = UI()

    def reset(self, to_menu=False):
        self.score = 0
        self.time_score = 0.0

        self.player.reset()
        self.obstacles.reset()

        self.state = GameState.MENU if to_menu else GameState.PLAY

    def start_game(self):
        self.reset(to_menu=False)

    def restart(self):
        self.reset(to_menu=False)

    def back_to_menu(self):
        self.reset(to_menu=True)

    def game_over(self):
        self.state = GameState.GAME_OVER

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                elif self.state == GameState.PLAY:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.restart()
                    elif event.key == pygame.K_m:
                        self.back_to_menu()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        
    def update(self, dt):
        if self.state != GameState.PLAY:
            return

        self.time_score += dt
        self.score = int(self.time_score)

        self.road.update(dt)
        self.player.update(dt)
        self.obstacles.update(dt)

        if self.obstacles.check_collision(self.player):
            self.game_over()
