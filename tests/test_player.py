import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pygame
import pytest
from player import PlayerCar


@pytest.fixture
def player():
    pygame.init()
    return PlayerCar(100, 200, 10)


class FakeKeys:
    def __init__(self, pressed_keys=None):
        self.pressed_keys = pressed_keys or set()

    def __getitem__(self, key):
        return key in self.pressed_keys


def test_player_initial_rect(player):
    assert player.rect.x == 100
    assert player.rect.y == 200
    assert player.rect.width == 50
    assert player.rect.height == 100


def test_move_left(player, monkeypatch):
    old_x = player.rect.x

    monkeypatch.setattr(
        pygame.key,
        "get_pressed",
        lambda: FakeKeys({pygame.K_LEFT})
    )

    player.handle_input(0, 500)

    assert player.rect.x == old_x - 10


def test_move_right(player, monkeypatch):
    old_x = player.rect.x

    monkeypatch.setattr(
        pygame.key,
        "get_pressed",
        lambda: FakeKeys({pygame.K_RIGHT})
    )

    player.handle_input(0, 500)

    assert player.rect.x == old_x + 10


def test_left_bound(player, monkeypatch):
    player.rect.x = 0

    monkeypatch.setattr(
        pygame.key,
        "get_pressed",
        lambda: FakeKeys({pygame.K_LEFT})
    )

    player.handle_input(0, 500)

    assert player.rect.x == 0


def test_right_bound(player, monkeypatch):
    player.rect.x = 500 - player.rect.width

    monkeypatch.setattr(
        pygame.key,
        "get_pressed",
        lambda: FakeKeys({pygame.K_RIGHT})
    )

    player.handle_input(0, 500)

    assert player.rect.x == 500 - player.rect.width


def test_reset(player):
    player.rect.x = 300
    player.rect.y = 400

    player.reset(100, 200)

    assert player.rect.x == 100
    assert player.rect.y == 200


@pytest.mark.parametrize(
    "start_x, keys, expected_x",
    [
        (100, {pygame.K_LEFT}, 90),
        (100, {pygame.K_RIGHT}, 110),
        (0, {pygame.K_LEFT}, 0),
        (450, {pygame.K_RIGHT}, 450),
    ]
)
def test_handle_input_parametrize(start_x, keys, expected_x, player, monkeypatch):
    player.rect.x = start_x

    monkeypatch.setattr(
        pygame.key,
        "get_pressed",
        lambda: FakeKeys(keys)
    )

    player.handle_input(0, 500)

    assert player.rect.x == expected_x