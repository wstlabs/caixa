import pytest
from typing import Any
from caixa.enum import StrEnum


def dump(item: any, label: str = 'item'):
    print(f"{label} = {item}, type(item) = {type(item)}, id = {id(item)}")
    print(f'{label}.__class__ = ', item.__class__)
    print(f'{label}.__bases__ = ', item.__class__.__bases__)
    status = isinstance(item, str) 
    print(f'{label}.is_str = {status}') 

def describe(obj: Any) -> str:
    return f"id={id(obj)}, type={type(obj)}, object={obj})"

def test_basics():
    """A minimal smoketest of basic class characteristics"""
    tags = list("abcde")
    Foo = StrEnum("Foo", tags) 
    # print(f"Foo.__bases__ = {Foo.__bases__}")
    # print(f"Foo.__module__ = {Foo.__module__}")
    # print([x for x in Foo])
    assert tags == list(Foo)
    a1 = Foo("a")
    a2 = Foo("a")
    print(f"a1.__class__ = {a1.__class__}")
    print('a1', describe(a1))
    print('a2', describe(a1))
    assert isinstance(a1, str)
    assert id(a1) == id(a2)
    assert 'a' in Foo
    assert 'x' not in Foo
    assert a1.position() == 1

def test_outside():
    Goo = StrEnum("Goo", list("abcde")) 
    with pytest.raises(ValueError):
        Goo("x")


def main():
    test_basics()
    test_outside()

if __name__ == '__main__':
    main()

