import time
from functools import wraps
from typing import Callable, Any

"""
Provides decorators for creating easy wrappers to measure the execution time of an input function. 
""" 

# We start with argless versions of the dual-purpose `timed`, which can also be imported
# if people like their signatures better.

def timed_without_return(func: Callable) -> Callable:
    """
    A simple timing decorator for a function with an empty return signature. 
    Equivalent to @timed(bare=False) or @timed().

    Example: 
        @timed_without_return
        def foobar(args: Any) -> None 
            do_something()

        delta = foobar(args)
        print(f"Did that in {delta} sec.")
    """
    @wraps(func)
    def called(*args, **kwargs) -> float: 
        t0 = time.time()
        func(*args, **kwargs)
        delta = time.time() - t0
        return delta
    return called

def timed_with_return(func: Callable) -> Callable:
    """
    A simple timing decorator for a function with a single-valued (non-tuple) return signature. 
    Equivalent to @timed(bare=True).

        @timed_with_return
        def foobar(args: Any) -> Any:
           return thing

        (delta, thing) = foobar(args)
        print(f"Got {thing} in {delta} sec.")
    """
    @wraps(func)
    def called(*args, **kwargs) -> tuple[float, Any]: 
        t0 = time.time()
        x = func(*args, **kwargs)
        delta = time.time() - t0
        return (delta, x)
    return called

def timed(bare: bool = False) -> Callable:
    """
    A simple timing decorator, which adjusts its returned signature according to the 
    signature of the calling function (as specified by the 'bare' flag).

    Returns:

        Either `delta` or the tuple `(delta, x)` depending on return signature above.
        Where `delta` is the elapsed real time in seconds.

    Examples (in pseudocode):

        @timed(bare=True)
        def foobar_without_return(x: Any) -> None:
            do_something() 

        delta = foobar(blah)

        @timed(bare=False)  # or timed()
        def foobar_with_return(x: Any) -> None:
            return y

        (delta, y) = foobar_with_return(x)

    Multi-valued returns are unpacked in the natural way:

        @timed(bare=False)
        def foobar_with_return(junk: Any) -> None:
            return x, y, z 

        (delta, (x, y, z)) = foobar_with_return(junk)

    Note that you still need the calling parens on the decorator even if the `bare`
    argument is not supplied.  So while calling the decrator without the parens will
    still compile:

        @timed
        def foobar(args: Any)
            ...

    When run dynamically it will get confused about what it's being called on, which will trigger 
    a TypeError in the calling context. 
    """
    if bare:
        return timed_without_return
    else:
        return timed_with_return

