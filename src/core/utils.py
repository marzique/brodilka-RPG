import pygame


def draw_outline(screen, image, topleft):
    """Draw outline of the image. Useful for collision testing."""
    top_rect = image.get_rect(topleft=topleft)
    pygame.draw.rect(screen, (255, 255, 255), top_rect, 1)
