import pygame

from pygame import DOUBLEBUF, QUIT
from pygame.constants import HWSURFACE

from .constants import WIDTH, HEIGHT
from .states import state_factory


class Control:
    WINDOW_SETTINGS = pygame.SCALED | HWSURFACE | DOUBLEBUF  # | pygame.NOFRAME

    """Main class of the game that implements game loop pattern."""
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), self.WINDOW_SETTINGS)
        self.running = True
        self.fps = 144
        self.clock = pygame.time.Clock()
        self.state = state_factory('Dungeon')
        self.state.game = self

    def main_loop(self):
        """
        Main game method that encapsulates 3 steps performed on every iteration:
        1) process client input;
        2) update game state;
        3) render state to the screen
        """
        while self.running:
            self.dt = self.clock.tick(self.fps) / 1000
            self.process_input()
            self.update()
            self.render()

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
        self.state.render(self.screen)
        pygame.display.flip()
