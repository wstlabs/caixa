
def find_not(string: str, target: str) -> int:
    """Analagous to `str.find` but returns the index for the first character in the
    given string that does not match the given target character.

    Args:
       'string' - a string of any length
       'target' - a string of length 1 (representing a single character)

    Return:
       An integer > 0 if the string contains at least one character not equal to the target
       -1 otherwise (if the string is either empty, or is equal to repeated instances of the target character)
    """
    if len(target) != 1:
        raise ValueError("invalid usage - 'target' should be string of length 1")
    i: int
    char: str
    for (i, char) in enumerate(string):
        if char != target:
            return i
    return -1


