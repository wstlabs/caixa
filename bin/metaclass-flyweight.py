"""Demonstrates the Flyweight mixin in caixa.metaclasses"""

from typing import Optional, Any
from caixa.metaclasses import Flyweight

def describe(label: str = 'object', obj: Optional[Any]= None) -> str:
    return f"id={id(obj)} type={type(obj)} object={obj}"

class A(str, metaclass=Flyweight): 
    pass

class B(A):
    pass

class C(metaclass=Flyweight): 
    foo: Optional[str] = None
    bar: Optional[int] = None

    def __init__(self, foo: Optional[str] = "junk", bar: Optional[int] = None) -> None:
        self.foo = foo
        self.bar = bar

    def __str__(self) -> str:
        return f"C(foo='{self.foo}',bar={self.bar})"


def demo_simple():
    a1 = A('foo')
    a2 = A('foo')
    print(describe('A',A))
    print(describe('a1',a1))
    print(describe('a2',a2))

def demo_inherit():
    b1 = B('ook')
    b2 = B('ook')
    print(describe('b1',b1))
    print(describe('b2',b2))
    b3 = B('foo')
    b4 = B('foo')
    print(describe('b3',b3))
    print(describe('b4',b4))

def demo_other():
    c1 = C('woo',3)
    c2 = C('woo',3)
    c3 = C(foo='woo',bar=3)
    print(describe('c1',c1))
    print(describe('c2',c2))
    print(describe('c3',c3))

def main():
    demo_simple()
    demo_inherit()
    demo_other()

if __name__ == '__main__':
    main()





"""
class B(A, metaclass=Flyweight):
    pass

class C(str, metaclass=Flyweight):
    pass
"""

