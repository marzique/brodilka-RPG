from functools import wraps

from src.constants import DEBUG


def debug(func):
    """Decorator that executes decorated method only in DEBUG mode."""
    @wraps(func)
    def decorated(*args, **kwargs):
        if DEBUG:
            func(*args, **kwargs)
    return decorated
