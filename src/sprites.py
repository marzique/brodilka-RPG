import pygame

from src.constants import TILE_SIZE_PX


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE_PX
        self.rect.y = y * TILE_SIZE_PX


class AnimatedSprite(BaseSprite):
    pass


class Tile(BaseSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.id = kwargs.get('id')
        self.is_wall = kwargs.get('wall', False)
