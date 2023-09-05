"""
Provides the factory class StrEnum, analogous to enum.IntEnum.
See the docstring to the StrEnum class for details."""
from typing import type, Iterator, Any

def dump(item: Any, label: str = 'item'):
    print(f"{label} = {item}, type(item) = {type(item)}, id = {id(item)}")
    print(f'{label}.__class__ = ', item.__class__)
    print(f'{label}.__bases__ = ', item.__class__.__bases__)
    status = isinstance(item, str) 
    print(f'{label}.is_str = {status}') 

"""
These next several methods support our factory class StrEnum below.

The main thing to understand is that the new classes that we create are produced not
declaratively (as in regular Python syntax) but rather are assembled directory by assiging 
appropriate elements in the classes dunder-dicts (which is sometimes called the "decorator
pattern").
"""

REG: dict[type, dict] = {}
def _register(cls: type, tags: List[str]) -> None:
    if cls in REG:
        raise ValueError(f"invalid usage - StrEnum class '{cls}' already registered") 
    REG[cls] = {'index': {}, 'memo': {}}
    for (i, tag) in enumerate(tags):
        pos = i+1
        if not isinstance(tag, str):
            raise ValueError(f"cannot build - expected string instance at position={pos}, got {type(tag)}")
        if tag in REG[cls]['index']:
            raise ValueError(f"cannot build - duplicate tag='{tag}' found at position={pos}")
        REG[cls]['index'][str(tag)] = pos

def _enumerate(cls: type) -> Iterator[Any]:
    if cls not in REG:
        raise ValueError(f"invalid usage - StrEnum class '{cls}' not yet registered") 
    for tag in REG[cls]['index']:
        yield strenum_instance(cls, tag)

#
# Instance methods for providing classes. 
#

def strenum_instance(cls, tag: str):
    """
    Returns (and if necessary, creates) a singleton instance in the given StrEnum class `cls`
    for the given string `tag`.  
    """
    if cls not in REG:
        raise RuntimeError("invalid usage - class '{cls}' not registered")
    if tag not in REG[cls]['index']:
        raise ValueError(f"'{tag}' is not a valid instance of {cls}")
    if tag not in REG[cls]['memo']:
        REG[cls]['memo'][tag] = str.__new__(cls, tag)
    return REG[cls]['memo'][tag]
    # print(f"strenum_instance: cls = {cls}")
    # print(f"strenum_instance: type(cls) = {type(cls)}")
    # print(f"strenum_instance: tag = %r" % tag)
    # nifty = str.__new__(cls, tag)
    # dump(nifty,'nifty')
    # REG[cls]['memo'][tag] = nifty 

def strenum_position(self) -> None:
    """Given a string :tag, returns an integer representing its position (or index) in the sequence 
    which defines this `StrEnum` class.  Following the convention of `enum.IntEnum`, this index 
    starts with 1 rather than 0.  If the `tag` is not in our initial sequence, an exception
    is raised."""
    cls, tag = type(self), str(self)
    position = REG[cls]['index'].get(tag)
    if position is None:
        raise RuntimeError("invalid state - no index record for tag='{tag}', cls={cls}") 
    return position
    # print(f"strenum_position id = {id(self)}")
    # print(f"strenum_position self = {self} of type={type(self)}")
    # print(f"strenum_position tag = '{tag}' of type={type(tag)}")

def strenum_value(self) -> str:
    return str(self)


"""
A ready-made dict of attributes for providing class instances.
This ends up being copied and passed along in StrEnum.__new__ 
"""
ATTRS: Dict[str, Any] = {}
ATTRS['__new__'] = strenum_instance
ATTRS['position'] = strenum_position
ATTRS['value'] = strenum_value

class StrEnum(type):
    """The factory class, class StrEnum, analogous to enum.IntEnum.
     
    By "factory class" we mean (in our unofficial terminology) a class whose constructor 
    returns not an instance of its own class, but rather creates an entirely new class
    based on the given :name and list of :tags. 

    The `namedtuple` constructor in the standard library workds in this way, as does
    the `enum.IntEnum` class whose interface we attempt to follow as closely as possible.

    The difference is our resultant classes inherit from `str` rather than `int`, and the 
    input sequence of admissible values are based on `str` as well.
    Typical usage might go like this:

        values = ['a', 'b', 'c', 'd']
        Foo = StrEnum('Foo', values)
        a = Foo('a')
        print(a, instance(a,str)) # 'a', True 
        print([_ for _ in Foo])

    Behaves in all the (important) ways you'd expect an Enum class to behave:
    - The elements are singletons (and only created when first accessed).
    - Once initialzed with a given value set, only elements corresponding to those
      values can be referenced / instantiated.

    However there are some crucial differences / limitations:
    - The .value property is supported, but not the .name property 
    - Attribute-level access is not supported in the way it for Enum/IntEnum objects.
      That's because we allow arbitrary strings as elements (which in general are not 
      necessarily valid python identifiers, hence not permitted as attributes).
    - So as a result, elements are referenced only via the constructor."""
    def __new__(mcls, name: str, tags: List[str], attrs: dict = None):
        if name.startswith('None'):
            return None
        bases = (str,)
        attrs = {} if attrs is None else attrs
        attrs = {**ATTRS, **attrs}
        newcls = super(StrEnum, mcls).__new__(mcls, name, bases, attrs)
        _register(newcls, tags)
        return newcls

    def __init__(self, name: str, bases: tuple = None, attrs: dict = None): 
        pass

    def __iter__(self):
         return _enumerate(self)

