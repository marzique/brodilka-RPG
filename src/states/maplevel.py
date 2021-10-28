import os

import pygame
from pytmx import load_pygame

from src.characters import Player, BaseCharacter
from src.constants import TILE_SIZE_PX, DEBUG, TileTypes
from src.core.utils import draw_outline
from src.states.base_state import BaseState


class MapLevel(BaseState):
    """Base class for all game levels a.k.a. maps."""
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.tilemap = self.load_tilemap(name)
        self.player = Player('Tester', coords=(50, 150), map_level=self)
        self.mobs = self.generate_mobs()

    @staticmethod
    def load_tilemap(name):
        path = os.path.join(os.getcwd(), 'data', 'tilesheets', f'{name}.tmx')
        tilemap = load_pygame(path)
        return tilemap

    def process_input(self, event):
        super().process_input(event)
        self.player.process_input(event)

    def update(self):
        super().update()
        self.player.update()

    def is_blocker(self, x, y):
        tile_properties = {}
        try:
            tile_properties = self.tilemap.get_tile_properties(x // TILE_SIZE_PX, y // TILE_SIZE_PX, 0) or {}
        except ValueError:
            tile_properties = {}
        finally:
            if tile_properties.get('type') == TileTypes.BLOCKER:
                return True
            return False

    @staticmethod
    def on_the_same_line(tile: pygame.Rect, player: BaseCharacter):
        if tile.center[1] - player.rect.center[1] < (TILE_SIZE_PX // 2):
            return True
        return False

    @staticmethod
    def in_the_same_row(tile: pygame.Rect, player: BaseCharacter):
        if tile.center[0] - player.rect.center[0] < (TILE_SIZE_PX // 2):
            return True
        return False

    def generate_mobs(self):
        # TODO: generate all types of objects present in level
        button = pygame.Rect(500, 500, TILE_SIZE_PX, TILE_SIZE_PX)
        mobs = [button]
        return mobs

    def render(self, screen):
        self.render_tilemap(screen)
        self.player.render(screen)
        self.render_mobs(screen)

    def render_tilemap(self, screen):
        for layer in self.tilemap.layers:
            for x, y, image in layer.tiles():
                topleft = (x * TILE_SIZE_PX, y * TILE_SIZE_PX)
                screen.blit(image, topleft)
                if DEBUG:
                    draw_outline(screen, image, topleft)

    def render_mobs(self, screen):
        for mob in self.mobs:
            pygame.draw.rect(screen, [173, 100, 170], mob, 1)

