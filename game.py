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