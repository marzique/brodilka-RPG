import pygame

from src.constants import TILE_SIZE_PX


class Blocker(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE_PX
        self.rect.y = y * TILE_SIZE_PX
