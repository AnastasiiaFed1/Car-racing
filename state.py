from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    PLAY = auto()
    GAME_OVER = auto()