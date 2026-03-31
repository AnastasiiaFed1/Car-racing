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
    def draw_menu(self):
        title = self.font.render("CAR RACING", True, TEXT_COLOR)
        text = self.small_font.render("SPACE - start   ESC - quit", True, TEXT_COLOR)

        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 200))
        self.screen.blit(text, (SCREEN_W // 2 - text.get_width() // 2, 280))

    def draw_game_over(self):
        title = self.font.render("GAME OVER", True, TEXT_COLOR)
        score_text = self.small_font.render(f"Score: {self.score}", True, TEXT_COLOR)
        info = self.small_font.render("R - restart   M - menu   ESC - quit", True, TEXT_COLOR)

        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 200))
        self.screen.blit(score_text, (SCREEN_W // 2 - score_text.get_width() // 2, 260))
        self.screen.blit(info, (SCREEN_W // 2 - info.get_width() // 2, 320))

    def draw_play(self):
        self.road.draw(self.screen)
        self.player.draw(self.screen)
        self.obstacles.draw(self.screen)

        score_text = self.small_font.render(f"Time: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (20, 20))

    def draw(self):
        self.screen.fill(BG_COLOR)

        if self.state == GameState.MENU:
            self.draw_menu()

        elif self.state == GameState.PLAY:
            self.draw_play()

        elif self.state == GameState.GAME_OVER:
            self.road.draw(self.screen)
            self.player.draw(self.screen)
            self.obstacles.draw(self.screen)
            self.draw_game_over()

        pygame.display.flip()
