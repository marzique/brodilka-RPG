import pygame

from . import constants


class BaseProjective:
    SPEED = 0
    IMAGE_FILE = ''

    def __init__(self, x_out, y_out, direction):
        self.x = x_out
        self.start_x = self.x
        self.y = y_out
        self.start_y = self.y
        self.direction = direction
        self.speed = self.SPEED
        self.image = pygame.image.load(self.IMAGE_FILE).convert_alpha()
        self.subimages = [self.image.subsurface(0, 8, 26, 9),
                          self.image.subsurface(27, 8, 26, 9),
                          self.image.subsurface(54, 0, 9, 25),
                          self.image.subsurface(65, 0, 9, 25)]

    def render(self, screen):
        screen.blit(self.subimages[self.direction], (self.x, self.y))

    def move(self):
        if self.direction == constants.CHAR_R:
            self.x += self.SPEED
        if self.direction == constants.CHAR_L:
            self.x -= self.SPEED
        if self.direction == constants.CHAR_U:
            self.y -= self.SPEED
        if self.direction == constants.CHAR_D:
            self.y += self.SPEED


class Bullet(BaseProjective):
    IMAGE_FILE = 'data/BULLETS.png'
    SPEED = constants.BULLET_SPEED
