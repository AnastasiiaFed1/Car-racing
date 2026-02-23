import pygame


class Road:
    """
    Road renders:
    - grass background
    - asphalt road rectangle
    - borders
    - dashed lane separators that scroll down
    """

    def __init__(
        self,
        screen_w: int,
        screen_h: int,
        lane_count: int = 3,
        road_width_ratio: float = 0.60,
        border_width: int = 4,
        dash_len: int = 28,
        dash_gap: int = 22,
        scroll_multiplier: float = 1.0,
    ):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.lane_count = max(2, int(lane_count))

        self.road_w = int(screen_w * road_width_ratio)
        self.road_x = (screen_w - self.road_w) // 2
        self.road_rect = pygame.Rect(self.road_x, 0, self.road_w, screen_h)

        self.border_width = border_width
        self.dash_len = dash_len
        self.dash_gap = dash_gap
        self.scroll_multiplier = scroll_multiplier

        self._offset_y = 0.0

        # colors (simple defaults)
        self._grass = (18, 90, 28)
        self._asphalt = (48, 48, 54)
        self._border = (235, 235, 235)
        self._dash = (220, 220, 220)

    def update(self, dt: float, speed: float):
        """
        dt: seconds since last frame
        speed: game speed (any unit). Used to scroll the dashed lines.
        """
        step = float(speed) * float(self.scroll_multiplier) * float(dt)
        period = self.dash_len + self.dash_gap
        self._offset_y = (self._offset_y + step) % period

    def draw(self, surface: pygame.Surface):
        # grass
        surface.fill(self._grass)

        # asphalt
        pygame.draw.rect(surface, self._asphalt, self.road_rect)

        # borders
        left_x = self.road_x
        right_x = self.road_x + self.road_w
        pygame.draw.line(surface, self._border, (left_x, 0), (left_x, self.screen_h), self.border_width)
        pygame.draw.line(surface, self._border, (right_x, 0), (right_x, self.screen_h), self.border_width)

        # lane dashed lines
        lane_w = self.road_w / self.lane_count
        for i in range(1, self.lane_count):
            x = int(self.road_x + lane_w * i)
            self._draw_dashed_vertical(surface, x)

    def _draw_dashed_vertical(self, surface: pygame.Surface, x: int):
        period = self.dash_len + self.dash_gap
        y = -period + int(self._offset_y)

        while y < self.screen_h:
            pygame.draw.line(surface, self._dash, (x, y), (x, y + self.dash_len), 3)
            y += period