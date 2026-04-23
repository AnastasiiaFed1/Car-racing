from __future__ import annotations

import pygame

from player import PlayerCar
from obstacles import Spawner
from settings import SCREEN_W, SCREEN_H, FPS
from game.road import Road
from game.state import GameState
from game.ui import UI

PLAYER_W = 56
PLAYER_H = 100


class CarRacingGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Racing")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()

        self.road = Road(SCREEN_W, SCREEN_H)
        self.ui = UI(SCREEN_W, SCREEN_H)
        self.running = True
        self.max_speed = 18

        self.reset(to_menu=True)

    def reset(self, to_menu: bool = False):
        self.state = GameState.MENU if to_menu else GameState.PLAYING
        self.score = 0
        self.level = 1
        self.speed = 7.0
        self.lives = 1
        self.collision_flash = False
        self.spawner = Spawner(self.road)

        player_x = self.road.get_lane_center_x(1) - PLAYER_W // 2
        player_y = SCREEN_H - PLAYER_H - 20
        speed = self.speed
        self.player = PlayerCar(player_x, player_y, speed)

    def start_game(self):
        self.reset(to_menu=False)

    def toggle_pause(self):
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def back_to_menu(self):
        self.reset(to_menu=True)

    def restart(self):
        self.reset(to_menu=False)

    def update_level(self):
        self.level = 1 + self.score // 12
        self.speed = min(7.0 + self.level * 1.2, self.max_speed)

    def update_playing(self, dt: float):

        left_limit = self.road.road_x + 12
        right_limit = self.road.road_x + self.road.road_w - 12

        self.player.handle_input(left_limit, right_limit)
        self.road.update(dt, self.speed * 60)
        removed_count = self.spawner.update(dt, SCREEN_H, SCREEN_W)
        self.score += removed_count
        self.update_level()

        if self.spawner.check_all_collisions(self.player.rect):
            self.collision_flash = True
            self.state = GameState.GAME_OVER

    def draw(self):
        self.road.draw(self.screen)

        self.spawner.draw(self.screen)

        if self.state in (GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER):
            self.player.draw(self.screen)

        self.ui.draw(self.screen, self)
        pygame.display.flip()

    def handle_actions(self, actions: list[str]):
        for action in actions:
            if action == "QUIT":
                self.running = False
            elif action == "START":
                self.start_game()
            elif action == "RESTART":
                self.restart()
            elif action == "TOGGLE_PAUSE":
                self.toggle_pause()
            elif action == "BACK_TO_MENU":
                self.back_to_menu()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                self.handle_actions(self.ui.handle_event(event, self))

            if self.state == GameState.PLAYING:
                self.update_playing(dt)

            self.ui.update(dt, self)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    CarRacingGame().run()
