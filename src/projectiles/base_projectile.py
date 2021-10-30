import pygame

from src.constants import RIGHT, TOP, LEFT, BOTTOM, BULLET_DISTANCE


class BaseProjectile:
    SPEED = 0
    IMAGE_FILE = ''

    def __init__(self, x_out, y_out, direction):
        self.x = self.start_x = x_out
        self.y = self.start_y = y_out
        self.direction = direction
        self.speed = self.SPEED
        self.image = pygame.image.load(self.IMAGE_FILE).convert_alpha()
        self.subimages = [self.image.subsurface(54, 0, 9, 25),  # D
                          self.image.subsurface(65, 0, 9, 25),  # U
                          self.image.subsurface(0, 8, 26, 9),   # R
                          self.image.subsurface(27, 8, 26, 9)]  # L

    def render(self, screen):
        screen.blit(self.subimages[self.direction], (self.x, self.y))

    def move(self):
        if self.direction == RIGHT:
            self.x += self.speed
        if self.direction == LEFT:
            self.x -= self.speed
        if self.direction == TOP:
            self.y -= self.speed
        if self.direction == BOTTOM:
            self.y += self.speed

    def flew_away(self) -> bool:
        if self.x - self.start_x >= BULLET_DISTANCE:
            return True
        if self.y - self.start_y >= BULLET_DISTANCE:
            return True
        return False
