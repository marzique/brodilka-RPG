from .menu import MainMenu
from .level import Level


# String mapping of all game states.
# TODO: refactor
def get_state(name):
    states = {
        'MainMenu': MainMenu(),
        'Dungeon': Level('dungeon')
    }
    return states[name]


__all__ = ['get_state', 'MainMenu', 'Level']
