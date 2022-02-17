from typing import Callable

def memoize(function: Callable) -> Callable:
    """
    An extremely simple, general-purpose shallow memoizer.
    """
    cache = {}
    def wrapper(*args, **kwargs):
        key = tuple(args)
        if key not in cache:
            cache[key] = function(*args, **kwargs)
        return cache[key]
    return wrapper 

