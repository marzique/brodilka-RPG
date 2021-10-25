from .menu import MainMenu
from .levelmap import LevelMap


# String mapping of all game states.
# TODO: refactor
def get_state(name):
    states = {
        'MainMenu': MainMenu(),
        'Dungeon': LevelMap('level1')
    }
    return states[name]


__all__ = ['get_state', 'MainMenu', 'LevelMap']
