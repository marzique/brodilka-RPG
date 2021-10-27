from .menu import MainMenu
from .maplevel import MapLevel


# String mapping of all game states.
# TODO: refactor
def get_state(name):
    states = {
        'MainMenu': MainMenu(),
        'Dungeon': MapLevel('level1')
    }
    return states[name]


__all__ = ['get_state', 'MainMenu', 'MapLevel']
