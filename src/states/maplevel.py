import os

import pygame
from pygame.examples.joystick import WHITE
from pytmx import load_pygame

from src.characters import Player, BaseCharacter
from src.constants import TILE_SIZE_PX, DEBUG, TileTypes, WIDTH, HEIGHT, Colors
from src.core.utils import debug
from src.sprites import Blocker, Tile
from src.states.base_state import BaseState


class MapLevel(BaseState):
    def __init__(self, name):
        super().__init__()
        self.game = None  # will be set inside Control class
        self.name = name
        self.tilemap = self.load_tilemap(name)
        self.player = Player('Tester', coords=(50, 150), map_level=self)
        self.all_tiles = pygame.sprite.Group()
        self.blockers = pygame.sprite.Group()
        self.setup_tiles()
        self.width = self.tilemap.width * TILE_SIZE_PX
        self.height = self.tilemap.height * TILE_SIZE_PX
        self.camera = Camera(self.width, self.height)

    @staticmethod
    def load_tilemap(name):
        path = os.path.join(os.getcwd(), 'data', 'tilesheets', f'{name}.tmx')
        tilemap = load_pygame(path)
        return tilemap
    
    def setup_tiles(self):
        """Create blocker sprites and add them to blockers group"""
        blockers = []
        all_tiles = []
        for layer in self.tilemap.layers:
            print(list(layer.tiles()))
            for x, y, image in layer.tiles():
                all_tiles.append(Tile(image, x, y))
                if self.is_blocker(x, y):
                    blockers.append(Blocker(image, x, y))
        self.all_tiles.add(*all_tiles)
        self.blockers.add(*blockers)

    def process_input(self, event):
        super().process_input(event)
        self.player.process_input(event)

    def update(self):
        super().update()
        self.blockers.update()
        self.player.update()
        self.camera.update(self.player)

    def is_blocker(self, x: int, y: int) -> bool:
        try:
            tile_properties = self.tilemap.get_tile_properties(x, y, 0) or {}
            if tile_properties.get('type') == TileTypes.BLOCKER:
                return True
        except ValueError:
            return False
        return False

    def render(self, screen):
        self.render_tilemap(screen)
        self.player.render(screen)

    def render_tilemap(self, screen):

        # scrolling map (FIXME: blockers not moving)
        for sprite in self.all_tiles:
            screen.blit(sprite.image, self.camera.apply_offset(sprite))
        self.draw_player_border(screen)

    @debug
    def draw_player_border(self, screen):
        for sprite in self.all_tiles:
            if self.is_blocker(sprite.rect.x // 32, sprite.rect.y // 32):
                color = Colors.RED
            else:
                color = Colors.WHITE
            pygame.draw.rect(screen, color, sprite.rect, 1)


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply_offset(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = int(WIDTH / 2) - target.rect.x
        y = int(HEIGHT / 2) - target.rect.y

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)
