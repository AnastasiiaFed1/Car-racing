import pygame
from game.state import GameState


class UI:
    """
    UI renders:
    - HUD: score, speed, level
    - MENU screen
    - PAUSED overlay
    - GAME OVER screen
    - flash effect on collision (white overlay fading out)

    UI reads these fields from `game`:
    - game.state (GameState)
    - game.score (int)
    - game.speed (float)
    - game.level (int)  [optional, default 1]
    - game.collision_flash (bool) [optional, if True => flash and reset to False]
    """

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h

        pygame.font.init()
        self.font_hud = pygame.font.SysFont("arial", 22)
        self.font_mid = pygame.font.SysFont("arial", 24)
        self.font_big = pygame.font.SysFont("arial", 42, bold=True)
        self.font_title = pygame.font.SysFont("arial", 56, bold=True)

        # flash effect
        self.flash_alpha = 0  # 0..255
        self.flash_decay_per_sec = 420

        # reusable overlay
        self._overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)

    def handle_event(self, event: pygame.event.Event, game) -> list[str]:
        """
        Returns actions: START, RESTART, TOGGLE_PAUSE, BACK_TO_MENU, QUIT
        """
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
        # optional collision flag integration
        if getattr(game, "collision_flash", False):
            self.trigger_flash()
            game.collision_flash = False

        # decay flash
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, int(self.flash_alpha - self.flash_decay_per_sec * dt))

    def trigger_flash(self, alpha: int = 220):
        self.flash_alpha = max(self.flash_alpha, int(alpha))

    def draw(self, surface: pygame.Surface, game):
        # HUD visible in-game states
        if game.state in (GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER):
            self._draw_hud(surface, game)

        # overlays/screens
        if game.state == GameState.MENU:
            self._draw_menu(surface)
        elif game.state == GameState.PAUSED:
            self._draw_pause(surface)
        elif game.state == GameState.GAME_OVER:
            self._draw_game_over(surface, game)

        # flash always on top
        if self.flash_alpha > 0:
            self._overlay.fill((255, 255, 255, self.flash_alpha))
            surface.blit(self._overlay, (0, 0))

    def _draw_hud(self, surface: pygame.Surface, game):
        score = getattr(game, "score", 0)
        speed = getattr(game, "speed", 0.0)
        level = getattr(game, "level", 1)

        text = f"Score: {score}   Speed: {speed:.1f}   Level: {level}"
        img = self.font_hud.render(text, True, (240, 240, 240))
        surface.blit(img, (14, 12))

    def _dim(self, surface: pygame.Surface, alpha: int):
        self._overlay.fill((0, 0, 0, alpha))
        surface.blit(self._overlay, (0, 0))

    def _draw_center_block(self, surface: pygame.Surface, title: str, lines: list[str]):
        title_img = self.font_title.render(title, True, (245, 245, 245))
        title_rect = title_img.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 120))
        surface.blit(title_img, title_rect)

        y = self.screen_h // 2 - 40
        for line in lines:
            img = self.font_mid.render(line, True, (230, 230, 230))
            rect = img.get_rect(center=(self.screen_w // 2, y))
            surface.blit(img, rect)
            y += 32

    def _draw_menu(self, surface: pygame.Surface):
        self._dim(surface, 110)
        self._draw_center_block(surface, "CAR RACING", ["Enter — Start", "Esc — Quit"])

    def _draw_pause(self, surface: pygame.Surface):
        self._dim(surface, 140)
        pause_img = self.font_big.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_img.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 30))
        surface.blit(pause_img, pause_rect)

        hint = self.font_mid.render("P — Continue | Esc — Menu", True, (230, 230, 230))
        hint_rect = hint.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 20))
        surface.blit(hint, hint_rect)

    def _draw_game_over(self, surface: pygame.Surface, game):
        self._dim(surface, 150)
        score = getattr(game, "score", 0)

        over_img = self.font_big.render("GAME OVER", True, (255, 255, 255))
        over_rect = over_img.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 70))
        surface.blit(over_img, over_rect)

        score_img = self.font_mid.render(f"Score: {score}", True, (230, 230, 230))
        score_rect = score_img.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 25))
        surface.blit(score_img, score_rect)

        hint = self.font_mid.render("R — Restart | Esc — Menu", True, (230, 230, 230))
        hint_rect = hint.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 20))
        surface.blit(hint, hint_rect)