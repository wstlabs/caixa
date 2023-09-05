from typing import Any

REG: dict[type, dict[tuple,Any]] = {}
class Flyweight(type):
    """A simple flyweight mixin that works in the narrow use case in which the constructor is 
    called with positional arguments only.  That is, it memoizes only on the list of `args` passed, 
    but does not look at the `kwargs` dict at at all. 

    This of course poses considerable limits on its usage, as it has no way of recognizing that 
    a keyword invocation of the constructor, e.g. `Foo(color="blue",rank=3)` should return the
    same cached instance as would a positional invocation, e.g. `Foo("blue",3)`.  

    I has other limitations: it has no way of treating the logic of signatures with default 
    arguments, for example.

    But for the narrow use case above, it does seem to work.
    See the test suite for sample usage."""
    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in REG:
            REG[cls] = {}
        pk = tuple(args) 
        instance: Any = REG[cls].get(pk)
        if instance is None:
            instance = REG[cls][pk] = type.__call__(cls, *args, **kwargs)
        return instance

