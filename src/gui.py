import pygame

from src.constants import HEIGHT, WIDTH, HPMP_THICKNESS, Colors, Fonts, GOLD
from src.core.utils import add_text


class GUI:
    """Class for Player GUI interface layer."""
    def __init__(self, player):
        self.player = player
        self.height = HEIGHT
        self.width = WIDTH

    def render(self, screen):
        self.render_ui(screen)
        self.render_ammo(screen)

    def render_ui(self, screen):
        x_start = 10
        pygame.draw.line(
            screen, Colors.BLUE,
            (x_start, self.height - HPMP_THICKNESS),
            (x_start + self.player.mp, self.height - HPMP_THICKNESS),
            HPMP_THICKNESS
        )
        pygame.draw.line(
            screen, Colors.RED,
            (x_start, self.height - HPMP_THICKNESS * 2),
            (x_start + self.player.hp, self.height - HPMP_THICKNESS * 2),
            HPMP_THICKNESS
        )
        add_text(
            screen, f"lvl: {self.player.level}",
            x_start, self.height - 35,
            Fonts.main, 10, Colors.GOLD
        )

    def render_ammo(self, screen):
        if 10 - self.player.range_shots_limit >= 0:
            add_text(screen, "Ammo left: " + str(10 - self.player.range_shots_limit), WIDTH * 0.6,
                     HEIGHT - HEIGHT * 0.95, Fonts.main, 14, Colors.GOLD)
        else:
            add_text(screen, "Ammo left: " + '0', WIDTH * 0.6,
                     HEIGHT - HEIGHT * 0.95, Fonts.main, 14, Colors.RED)
            add_text(screen, "RELOADING...", WIDTH * 0.6,
                     HEIGHT - HEIGHT * 0.92, Fonts.regular, 14, Colors.RED)
