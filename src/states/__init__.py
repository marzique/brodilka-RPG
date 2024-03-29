from .menu import MainMenu
from .maplevel import MapLevel


def state_factory(name, **kwargs):
    """Return state class by name"""
    states = {
        'MainMenu': MainMenu(),
        'Dungeon': MapLevel('start_level', **kwargs)
    }
    return states[name]


__all__ = ['state_factory', 'MainMenu', 'MapLevel']
