import pygame

from src import constants
from src.control import Control


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(constants.WINDOW_NAME)
    game = Control()
    game.main_loop()
