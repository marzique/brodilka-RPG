import pygame

from src.constants import WINDOW_NAME
from src.control import Control


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)
    game = Control()
    game.main_loop()
