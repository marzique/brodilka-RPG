import pygame

from src.constants import WINDOW_NAME
from src.game import Game


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)
    game = Game()
    game.main_loop()
