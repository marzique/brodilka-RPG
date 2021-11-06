import pygame

from pygame import DOUBLEBUF, QUIT
from pygame.constants import HWSURFACE

from .constants import WIDTH, HEIGHT
from .states import state_factory
from .states.base_state import BaseState


class Control:
    """Main class of the game that implements game loop pattern."""
    WINDOW_SETTINGS = pygame.SCALED | HWSURFACE | DOUBLEBUF  # | pygame.NOFRAME

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), self.WINDOW_SETTINGS)
        self.running: bool = True
        self.dt: int = 0
        self.fps: int = 144
        self.clock = pygame.time.Clock()
        self.state: BaseState = state_factory('Dungeon', game=self)

    def main_loop(self) -> None:
        while self.running:
            self.dt = self.clock.tick(self.fps) / 1000
            self.process_input()
            self.update()
            self.render()

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            self.state.process_input(event)

    def update(self) -> None:
        self.state.update()

    def render(self) -> None:
        self.state.render(self.screen)
        pygame.display.flip()
