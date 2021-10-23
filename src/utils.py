import pygame


def add_text(screen, text, x_pos, y_pos, font_type, font_size, color):
    text = str(text)
    pygame.font.init()
    # font = pygame.font.Font(font_type, font_size)
    font = pygame.font.Font(font_type, font_size)
    text = font.render(text, False, color)
    screen.blit(text, (x_pos, y_pos))