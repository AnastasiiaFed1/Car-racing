import pygame

from game.state import GameState


class UI:
    """Renders HUD, menu, pause, game over, and collision flash."""

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h

        pygame.font.init()
        self.font_hud = pygame.font.SysFont("arial", 22)
        self.font_mid = pygame.font.SysFont("arial", 28)
        self.font_big = pygame.font.SysFont("arial", 44, bold=True)
        self.font_title = pygame.font.SysFont("arial", 60, bold=True)

        self.flash_alpha = 0
        self.flash_decay_per_sec = 420
        self._overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)

    def handle_event(self, event: pygame.event.Event, game) -> list[str]:
        actions: list[str] = []

        if event.type == pygame.QUIT:
            return ["QUIT"]

        if event.type != pygame.KEYDOWN:
            return actions

        key = event.key

        if game.state == GameState.MENU:
            if key == pygame.K_RETURN:
                actions.append("START")
            elif key == pygame.K_ESCAPE:
                actions.append("QUIT")

        elif game.state == GameState.PLAYING:
            if key == pygame.K_p:
                actions.append("TOGGLE_PAUSE")
            elif key == pygame.K_ESCAPE:
                actions.append("BACK_TO_MENU")

        elif game.state == GameState.PAUSED:
            if key == pygame.K_p:
                actions.append("TOGGLE_PAUSE")
            elif key == pygame.K_ESCAPE:
                actions.append("BACK_TO_MENU")

        elif game.state == GameState.GAME_OVER:
            if key == pygame.K_r:
                actions.append("RESTART")
            elif key == pygame.K_ESCAPE:
                actions.append("BACK_TO_MENU")

        return actions

    def update(self, dt: float, game):
        if getattr(game, "collision_flash", False):
            self.trigger_flash()
            game.collision_flash = False

        if self.flash_alpha > 0:
            self.flash_alpha = max(0, int(self.flash_alpha - self.flash_decay_per_sec * dt))

    def trigger_flash(self, alpha: int = 220):
        self.flash_alpha = max(self.flash_alpha, int(alpha))

    def draw(self, surface: pygame.Surface, game):
        if game.state in (GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER):
            self._draw_hud(surface, game)

        if game.state == GameState.MENU:
            self._draw_menu(surface)
        elif game.state == GameState.PAUSED:
            self._draw_pause(surface)
        elif game.state == GameState.GAME_OVER:
            self._draw_game_over(surface, game)

        if self.flash_alpha > 0:
            self._overlay.fill((255, 255, 255, self.flash_alpha))
            surface.blit(self._overlay, (0, 0))

    def _draw_hud(self, surface: pygame.Surface, game):
        score = getattr(game, "score", 0)
        speed = getattr(game, "speed", 0.0)
        level = getattr(game, "level", 1)
        lives = getattr(game, "lives", 1)

        text = f"Score: {score}   Speed: {speed:.0f}   Level: {level}   Lives: {lives}"
        img = self.font_hud.render(text, True, (240, 240, 240))
        surface.blit(img, (14, 12))

    def _dim(self, surface: pygame.Surface, alpha: int):
        self._overlay.fill((0, 0, 0, alpha))
        surface.blit(self._overlay, (0, 0))

    def _draw_center_block(self, surface: pygame.Surface, title: str, lines: list[str]):
        title_img = self.font_title.render(title, True, (245, 245, 245))
        title_rect = title_img.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 120))
        surface.blit(title_img, title_rect)

        y = self.screen_h // 2 - 30
        for line in lines:
            img = self.font_mid.render(line, True, (230, 230, 230))
            rect = img.get_rect(center=(self.screen_w // 2, y))
            surface.blit(img, rect)
            y += 38

    def _draw_menu(self, surface: pygame.Surface):
        self._dim(surface, 120)
        self._draw_center_block(
            surface,
            "CAR RACING",
            [
                "Left/Right - move",
                "P - pause",
                "Enter - start",
                "Esc - quit",
            ],
        )

    def _draw_pause(self, surface: pygame.Surface):
        self._dim(surface, 145)

        pause_img = self.font_big.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_img.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 30))
        surface.blit(pause_img, pause_rect)

        hint = self.font_mid.render("P - continue    Esc - menu", True, (230, 230, 230))
        hint_rect = hint.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 22))
        surface.blit(hint, hint_rect)

    def _draw_game_over(self, surface: pygame.Surface, game):
        self._dim(surface, 160)
        score = getattr(game, "score", 0)
        level = getattr(game, "level", 1)

        self._draw_center_block(
            surface,
            "GAME OVER",
            [
                f"Score: {score}",
                f"Level reached: {level}",
                "R - restart",
                "Esc - menu",
            ],
        )
