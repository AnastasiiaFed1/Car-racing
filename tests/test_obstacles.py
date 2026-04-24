import pytest
import pygame

from obstacles import Obstacle, Spawner


@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


#  Fake road
class FakeRoad:
    lane_count = 3

    def get_lane_center_x(self, lane):
        return 100 + lane * 100


# 1. spawn створює obstacle
def test_spawn_creates_obstacle():
    road = FakeRoad()
    spawner = Spawner(road)

    spawner.spawn(800)

    assert len(spawner.obstacles) == 1


# 2. obstacle рухається вниз
def test_obstacle_moves_down():
    obstacle = Obstacle(100, 0, speed=100, obs_type="car")

    obstacle.update(dt=1)

    assert obstacle.rect.y > 0


# 3. obstacle видаляється за екраном
def test_obstacle_removed_out_of_screen():
    road = FakeRoad()
    spawner = Spawner(road)

    obstacle = Obstacle(100, 1000, speed=100, obs_type="cone")
    spawner.obstacles.append(obstacle)

    removed = spawner.update(dt=1, screen_height=600, screen_width=800)

    assert obstacle not in spawner.obstacles
    assert removed == 1


# 4. перевірка колізії
def test_collision_detected():
    road = FakeRoad()
    spawner = Spawner(road)

    obstacle = Obstacle(100, 100, speed=0, obs_type="car")
    spawner.obstacles.append(obstacle)

    player_rect = pygame.Rect(100, 100, 50, 80)

    assert spawner.check_all_collisions(player_rect) is True


# 5. відсутність колізії
def test_no_collision():
    road = FakeRoad()
    spawner = Spawner(road)

    obstacle = Obstacle(100, 100, speed=0, obs_type="car")
    spawner.obstacles.append(obstacle)

    player_rect = pygame.Rect(300, 300, 50, 80)

    assert spawner.check_all_collisions(player_rect) is False


# 6. різні типи obstacle
def test_obstacle_types():
    car = Obstacle(0, 0, 100, "car")
    cone = Obstacle(0, 0, 100, "cone")

    assert car.obs_type == "car"
    assert cone.obs_type == "cone"
