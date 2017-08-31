import pygame
from Constants import *
import sys

class Projectives():
    def __init__(self, dir, image):
        self.dir = dir
        self.image = pygame.image.load(image).convert_alpha()
        self.subimages = []
        self.subimages.append(self.image.subsurface(0, 8, 26, 9))
        self.subimages.append(self.image.subsurface(27, 8, 26, 9))
        self.subimages.append(self.image.subsurface(54, 0, 9, 25))
        self.subimages.append(self.image.subsurface(65, 0, 9, 25))

    # прорисовка снаряда
    def render(self, screen):
        screen.blit(self.subimages[self.dir], (self.x, self.y))

    def move(self):
        if self.dir == CHAR_R:
            self.x += self.speed
        if self.dir == CHAR_L:
            self.x -= self.speed
        if self.dir == CHAR_U:
            self.y -= self.speed
        if self.dir == CHAR_D:
            self.y += self.speed

class Bullet(Projectives):
    def __init__(self, x_out, y_out, dir):
        self.x = x_out
        self.start_x = self.x
        self.y = y_out
        self.start_y = self.y
        self.image = 'data/BULLETS.png'
        self.speed = BULLET_SPEED
        Projectives.__init__(self,dir , self.image)
