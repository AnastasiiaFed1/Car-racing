from __future__ import annotations

import random
from dataclasses import dataclass

import pygame

from settings import SCREEN_W, SCREEN_H, FPS
from game.road import Road
from game.state import GameState
from game.ui import UI

PLAYER_W = 56
PLAYER_H = 100
ENEMY_W = 56
ENEMY_H = 100


@dataclass
class Car:
    rect: pygame.Rect
    color: tuple[int, int, int]
    speed: float = 0.0


class CarRacingGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Racing")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()

        self.road = Road(SCREEN_W, SCREEN_H)
        self.ui = UI(SCREEN_W, SCREEN_H)
        self.running = True

        self.enemy_spawn_timer = 0.0
        self.enemy_spawn_interval = 1.15
        self.player_move_speed = 360
        self.max_speed = 18

        self.reset(to_menu=True)

    def reset(self, to_menu: bool = False):
        self.state = GameState.MENU if to_menu else GameState.PLAYING
        self.score = 0
        self.level = 1
        self.speed = 7.0
        self.lives = 1
        self.collision_flash = False
        self.enemy_spawn_timer = 0.0
        self.enemy_spawn_interval = 1.15
        self.enemies: list[Car] = []

        player_x = self.road.get_lane_center_x(1) - PLAYER_W // 2
        player_y = SCREEN_H - PLAYER_H - 20
        self.player = Car(
            pygame.Rect(player_x, player_y, PLAYER_W, PLAYER_H),
            (40, 170, 255)
        )

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

    def spawn_enemy(self):
        lane = random.randint(0, self.road.lane_count - 1)
        x = self.road.get_lane_center_x(lane) - ENEMY_W // 2
        y = -ENEMY_H - random.randint(20, 220)
        speed = 240 + self.level * 28 + random.randint(0, 80)
        color = random.choice([
            (240, 70, 70),
            (255, 180, 0),
            (180, 90, 255),
            (70, 255, 130)
        ])
        self.enemies.append(Car(pygame.Rect(x, y, ENEMY_W, ENEMY_H), color, speed))

    def update_level(self):
        self.level = 1 + self.score // 12
        self.speed = min(7.0 + self.level * 1.2, self.max_speed)
        self.enemy_spawn_interval = max(0.45, 1.15 - self.level * 0.05)

    def update_playing(self, dt: float):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.player_move_speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.player_move_speed * dt

        self.player.rect.x += int(dx)

        left_limit = self.road.road_x + 12
        right_limit = self.road.road_x + self.road.road_w - self.player.rect.width - 12
        self.player.rect.x = max(left_limit, min(right_limit, self.player.rect.x))

        self.road.update(dt, self.speed * 60)

        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.enemy_spawn_timer = 0.0
            self.spawn_enemy()

        add_score = 0

        for enemy in self.enemies:
            enemy.rect.y += int(enemy.speed * dt)

        remaining = []
        for enemy in self.enemies:
            if enemy.rect.top > SCREEN_H:
                add_score += 1
            else:
                remaining.append(enemy)

        self.enemies = remaining
        self.score += add_score
        self.update_level()

        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.collision_flash = True
                self.state = GameState.GAME_OVER
                break

    def draw_car(self, car: Car, is_player: bool = False):
        body = car.rect
        pygame.draw.rect(self.screen, car.color, body, border_radius=10)

        window = pygame.Rect(body.x + 10, body.y + 12, body.w - 20, body.h // 4)
        pygame.draw.rect(self.screen, (210, 235, 255), window, border_radius=6)

        pygame.draw.rect(self.screen, (25, 25, 25), (body.x + 7, body.y + 16, 8, 18), border_radius=3)
        pygame.draw.rect(self.screen, (25, 25, 25), (body.right - 15, body.y + 16, 8, 18), border_radius=3)
        pygame.draw.rect(self.screen, (25, 25, 25), (body.x + 7, body.bottom - 34, 8, 18), border_radius=3)
        pygame.draw.rect(self.screen, (25, 25, 25), (body.right - 15, body.bottom - 34, 8, 18), border_radius=3)

        if is_player:
            pygame.draw.rect(self.screen, (255, 255, 255), body, 2, border_radius=10)

    def draw(self):
        self.road.draw(self.screen)

        for enemy in self.enemies:
            self.draw_car(enemy)

        if self.state in (GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER):
            self.draw_car(self.player, is_player=True)

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