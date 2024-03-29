import pygame

from src.constants import TILE_SIZE_PX


def add_text(screen, text, x_pos, y_pos, font_type, font_size, color, antialiasing=False):
    text = str(text)
    pygame.font.init()
    font = pygame.font.Font(font_type, font_size)
    text = font.render(text, antialiasing, color)
    screen.blit(text, (x_pos, y_pos))


def get_topleft(x, y):
    x = (int(x) // TILE_SIZE_PX) * TILE_SIZE_PX
    y = (int(y) // TILE_SIZE_PX) * TILE_SIZE_PX
    return x, y
