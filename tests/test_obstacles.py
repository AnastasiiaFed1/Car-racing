import pytest
import pygame
from obstacles import Obstacle, Spawner

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

class FakeRoad:
    lane_count = 3
    def get_lane_center_x(self, lane):
        return 100 + lane * 100

def test_obstacle_init():
    # Твій код очікує x, y, speed, obs_type
    obs = Obstacle(100, 200, 300, "car")
    assert obs.rect.x == 100
    assert obs.rect.y == 200
    assert obs.speed == 300
    assert obs.obs_type == "car"

def test_spawner_init():
    road = FakeRoad()
    spawner = Spawner(road)
    assert spawner.road.lane_count == 3
    assert len(spawner.obstacles) == 0

def test_collision_check():
    obs = Obstacle(100, 100, 0, "car")
    player_rect = pygame.Rect(100, 100, 50, 80)
    assert obs.check_collision(player_rect) is True
