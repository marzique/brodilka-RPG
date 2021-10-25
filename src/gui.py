import pygame

from src import constants
from src.utils import add_text


class GUI:
    """Class for Player GUI interface layer."""
    def __init__(self, player):
        self.player = player
        self.height = constants.HEIGHT
        self.width = constants.WIDTH

    def render(self, screen):
        self.render_ui(screen)
        self.render_ammo(screen)

    def render_ui(self, screen):
        x_start = 10
        pygame.draw.line(
            screen, constants.BLUE,
            (x_start, self.height - constants.HPMP_THICKNESS),
            (x_start + self.player.mp, self.height - constants.HPMP_THICKNESS),
            constants.HPMP_THICKNESS
        )
        pygame.draw.line(
            screen, constants.RED,
            (x_start, self.height - constants.HPMP_THICKNESS * 2),
            (x_start + self.player.hp, self.height - constants.HPMP_THICKNESS * 2),
            constants.HPMP_THICKNESS
        )
        add_text(
            screen, f"Level: {self.player.level}",
            self.player.x, self.player.y - 20,
            constants.FONT1, 10, constants.GOLD
        )

    def render_ammo(self, screen):
        if 10 - self.player.range_shots_limit >= 0:
            add_text(screen, "Ammo left: " + str(10 - self.player.range_shots_limit), constants.WIDTH * 0.6,
                     constants.HEIGHT - constants.HEIGHT * 0.95, constants.FONT1, 20, constants.WHITE)
        else:
            add_text(screen, "Ammo left: " + '0', constants.WIDTH * 0.6,
                     constants.HEIGHT - constants.HEIGHT * 0.95, constants.FONT1, 20, constants.RED)
            add_text(screen, "RELOADING...", constants.WIDTH * 0.6,
                     constants.HEIGHT - constants.HEIGHT * 0.92, constants.FONT1, 20, constants.RED)
