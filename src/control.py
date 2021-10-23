import pygame

from pygame import DOUBLEBUF, QUIT
from pygame.constants import HWSURFACE

from .import constants
from .states import get_state


button = pygame.Rect(500, 500, 50, 50)


class Control:
    """Main class of the game that implements game loop pattern."""
    def __init__(self):
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), HWSURFACE | DOUBLEBUF)
        self.running = True
        self.background = pygame.image.load(constants.BACKGROUND)
        self.fps = 144
        self.clock = pygame.time.Clock()
        self.state = get_state('Dungeon')
        pygame.init()
        pygame.display.set_caption(constants.WINDOW_NAME)

    def main_loop(self):
        """
        Main game method that encapsulates 3 steps performed on every iteration:
        1) process client input;
        2) update game state;
        3) render new frame.
        """
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(self.fps)

    def process_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = pygame.mouse.get_pos()  # gets mouse position
            #     if button.collidepoint(mouse_pos):
            #         print('button was pressed at {0}'.format(mouse_pos))
            self.state.process_input(event)

    def update(self):
        self.state.update()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.state.render(self.screen)
        self.render_button()
        pygame.display.update()

    def render_button(self):
        pygame.draw.rect(self.screen, [173, 100, 170], button, 5)
