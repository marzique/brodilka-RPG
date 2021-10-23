from abc import ABC, abstractmethod


class AbstractState(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def process_input(self, event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    @abstractmethod
    def startup(self):
        pass

    @abstractmethod
    def cleanup(self):
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
        print(f'{type(self).__name__} performed process_input')

    def update(self):
        print(f'{type(self).__name__} performed update')

    def render(self, screen):
        print(f'{type(self).__name__} performed render')

    def startup(self):
        print(f'{type(self).__name__} performed startup')

    def cleanup(self):
        print(f'{type(self).__name__} performed cleanup')
