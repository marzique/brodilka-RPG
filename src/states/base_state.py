from abc import ABC, abstractmethod


class AbstractState(ABC):
    @abstractmethod
    def process_input(self, event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen):
        pass


class BaseState(AbstractState):
    """Base class for all game states"""
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.game_data = {}
        self.music = None
        self.music_title = None
        self.previous_music = None

    def process_input(self, event):
        # print(f'{type(self).__name__} performed process_input')
        pass

    def update(self):
        # print(f'{type(self).__name__} performed update')
        pass

    def render(self, screen):
        # print(f'{type(self).__name__} performed render')
        pass
