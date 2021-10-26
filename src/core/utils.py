import pygame


def draw_outline(screen, image, topleft, color=(255, 255, 255)):
    """Draw outline of the image. Useful for collision testing."""
    top_rect = image.get_rect(topleft=topleft)
    pygame.draw.rect(screen, color, top_rect, 1)
