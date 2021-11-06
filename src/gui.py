import pygame

from src.constants import HEIGHT, WIDTH, HPMP_THICKNESS, Colors, Fonts, GOLD
from src.core.utils import add_text


class GUI:
    """Class for Player GUI interface layer."""
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.height = HEIGHT
        self.width = WIDTH
        self.x_offset = -self.player.offset[0]
        self.y_offset = -self.player.offset[1]

    def render(self, canvas):
        self.render_ui(canvas)
        self.render_ammo(canvas)

    def render_ui(self, canvas):
        x_start = self.x_offset + 10
        y_start = self.screen_rect.height + self.y_offset - HPMP_THICKNESS
        pygame.draw.line(
            canvas, Colors.BLUE,
            (x_start, y_start - HPMP_THICKNESS),
            (x_start + self.player.mp, y_start - HPMP_THICKNESS),
            HPMP_THICKNESS
        )
        pygame.draw.line(
            canvas, Colors.RED,
            (x_start, y_start),
            (x_start + self.player.hp, y_start),
            HPMP_THICKNESS
        )
        add_text(
            canvas, f"lvl: {self.player.level}",
            x_start, self.screen_rect.height + self.y_offset - 35,
            Fonts.main, 10, Colors.GOLD
        )

    def render_ammo(self, canvas):
        if 10 - self.player.range_shots_limit >= 0:
            add_text(canvas, "Ammo left: " + str(10 - self.player.range_shots_limit), WIDTH * 0.6,
                     HEIGHT - HEIGHT * 0.95, Fonts.main, 14, Colors.GOLD)
        else:
            add_text(canvas, "Ammo left: " + '0', WIDTH * 0.6,
                     HEIGHT - HEIGHT * 0.95, Fonts.main, 14, Colors.RED)
            add_text(canvas, "RELOADING...", WIDTH * 0.6,
                     HEIGHT - HEIGHT * 0.92, Fonts.regular, 14, Colors.RED)
