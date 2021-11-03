from .menu import MainMenu
from .maplevel import MapLevel


def state_factory(name):
    """Return state class by name"""
    states = {
        'MainMenu': MainMenu(),
        'Dungeon': MapLevel('level1')
    }
    return states[name]


__all__ = ['state_factory', 'MainMenu', 'MapLevel']
