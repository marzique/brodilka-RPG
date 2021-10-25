import os

import pygame
from pytmx import load_pygame

from src import constants
from src.characters import Player
from src.constants import TILE_SIZE_PX
from src.core.utils import draw_outline
from src.states.base_state import BaseState


class LevelMap(BaseState):
    """Base class for all game levels a.k.a. maps."""
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.tilemap = self.load_tilemap(name)
        self.player = Player('Tester', coords=(50, 50))
        self.colliding_objects = [self.player]
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
        self.handle_collissions(self.tilemap)

    def handle_collissions(self, tilemap):
        for obj in self.colliding_objects:
            obj.handle_collissions(tilemap)

    def generate_mobs(self):
        # TODO: generate all types of objects present in level
        button = pygame.Rect(500, 500, TILE_SIZE_PX, TILE_SIZE_PX)
        mobs = [button]
        # TODO: objects must have handle_collissions()
        # self.colliding_objects += mobs
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
                if constants.DEBUG:
                    draw_outline(screen, image, topleft)

    def render_mobs(self, screen):
        for mob in self.mobs:
            pygame.draw.rect(screen, [173, 100, 170], mob, 1)

    def startup(self):
        super().startup()

    def cleanup(self):
        super().cleanup()
