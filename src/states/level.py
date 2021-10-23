from src import constants
from src.characters import Player
from src.states.base_state import BaseState


class Level(BaseState):
    """Base class for all game levels a.k.a. maps."""
    def __init__(self, name, battles=False):
        super().__init__()
        self.name = name
        self.map = self.load_map(name)
        self.player = Player(constants.PLAYER_NAME)

    @staticmethod
    def load_map(name):
        """Load tilesheet file by name"""
        return 'TODO'

    def process_input(self, event):
        super().process_input(event)
        self.player.process_input(event)

    def update(self):
        super().update()
        self.player.update()

    def render(self, screen):
        super().render(screen)
        self.player.render(screen)

    def startup(self):
        super().startup()

    def cleanup(self):
        super().cleanup()
