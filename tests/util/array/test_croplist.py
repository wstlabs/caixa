from caixa.util.array import croplist

"""
Very rudimentary
"""

def test_croplist():
    assert croplist(['a', 'b', 'c']) == "['a', 'b', 'c']"
    assert croplist(['a', 'b', 'c'], 1) == "['a' ... 'c']"
    assert croplist([]) == "[]"


