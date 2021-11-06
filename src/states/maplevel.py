import os

import pygame
from pygame import Surface
from pytmx import load_pygame, TiledMap

from src.characters import Player
from src.constants import TILE_SIZE_PX, WIDTH, HEIGHT, Colors
from src.core.utils import debug
from src.gui import GUI
from src.sprites import Tile
from src.states.base_state import BaseState


class MapLevel(BaseState):
    """State that represents game level."""
    def __init__(self, name, **kwargs):
        super().__init__()
        self.game = kwargs.get('game')
        self.name: str = name
        self.tilemap: TiledMap = self.load_tilemap(name)
        self.player = Player('Tester', coords=(50, 150), map_level=self)
        self.all_tiles = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.setup_tiles()
        self.width: int = self.tilemap.width * TILE_SIZE_PX
        self.height: int = self.tilemap.height * TILE_SIZE_PX
        self.camera = Camera(self.width, self.height)
        self.canvas = Surface((self.width, self.height))
        self.interface = GUI(self.player, self.game.screen)

    @staticmethod
    def load_tilemap(name: str) -> TiledMap:
        """Load *.tmx map data"""
        path = os.path.join(os.getcwd(), 'data', 'tilesheets', f'{name}.tmx')
        tilemap = load_pygame(path)
        return tilemap
    
    def setup_tiles(self) -> None:
        """Create sprite for each tile and store them in groups"""
        for i, layer in enumerate(self.tilemap.layers):
            for x, y, image in layer.tiles():
                kwargs = self.tilemap.get_tile_properties(x, y, i) or {}
                tile = Tile(image, x, y, **kwargs)
                self.all_tiles.add(tile)
                if tile.is_wall:
                    self.walls.add(tile)

    def process_input(self, event):
        super().process_input(event)
        self.player.process_input(event)

    def update(self):
        super().update()
        self.player.update()
        self.camera.update(self.player)
        self.update_player_offset()

    def update_player_offset(self):
        self.player.offset = self.camera.rect.topleft

    def render(self, screen):
        """Draws everything onto canvas, shifts canvas position to make player centered and draws canvas onto screen."""
        self.render_tilemap(self.canvas)
        self.player.render(self.canvas)
        self.interface.render(self.canvas)
        self.camera.scroll_canvas(self.canvas)
        screen.blit(self.canvas, self.canvas.get_rect())

    def render_tilemap(self, screen):
        self.all_tiles.draw(screen)
        self.draw_tile_borders(screen)

    @debug
    def draw_tile_borders(self, screen):
        for tile in self.all_tiles:
            if tile.is_wall:
                color = Colors.RED
            else:
                color = Colors.WHITE
            pygame.draw.rect(screen, color, tile.rect, 1)


class Camera:
    """Class that implements scrolling map feature that follows Player rect."""
    def __init__(self, width: int, height: int):
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def scroll_canvas(self, canvas: Surface) -> None:
        """Scroll canvas by offset"""
        return canvas.scroll(*self.rect.topleft)

    def update(self, player: Player) -> None:
        """Calculate offset of the camera."""
        x = int(WIDTH / 2) - player.rect.x
        y = int(HEIGHT / 2) - player.rect.y

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.rect = pygame.Rect(x, y, self.width, self.height)
