import re
from typing import Iterator, Tuple, Callable, Optional
from .patternbook import PatternBook

"""
Helper functions for string validation + profiling.

Most of these are, by themselves, basically trivial (some quite obviously so, e.g. 'is_empty').
But having them available as callables allows us to generate summary statistics (across the various 
criteria) in a consistent way.

In most of these functions, if a non-string argument is passed, a TypeError is thrown.
"""

PAT = {}
PAT['is-blank'] = re.compile('^\s+$')
PAT['has-whitespace-left'] = re.compile('^\s+')
PAT['has-whitespace-right'] = re.compile('^.*\s+$')
PAT['is-integer-like'] = re.compile('^[+-]{0,1}\d+$')
PAT['is-alphanumeric'] = re.compile('^[A-Za-z0-9]+$')
PATBOOK = PatternBook(PAT)

def assert_valid_separator(separator: str) -> None:
    if separator is None:
        raise ValueError("need a separator string")
    if len(separator) != 1:
        raise ValueError("invalid separator string '{string}'")

# TODO: memoize patterns; allow for varations of form based on options
def is_delim(string: str, separator: str) -> bool:
    """
    Returns True if the given :string is (naively) delimited by the given separator character.
    That is, having at least one inner instance, and no leading or trailing instances.

    By "naive" we mean it does not provide any special treatment for strings with nested 
    representations (e.g. involving quoting characters).  For that you need a proper CSV library.

    For example, if our sep string is the hyphen it will return True for the string "foo-bar" 
    but False for "foobar", "foo-", "-bar" as well as "foo--bar".  
    """
    assert_valid_separator(separator)
    qsep = f"\\{separator}" if separator in ("\\",'-') else separator
    pat = re.compile(f"^([^\s{qsep}]+{qsep})+([^\s{qsep}]+)$")
    return bool(pat.match(string))



def is_blank(s: str) -> bool:
    """
    Returns True if the string consists of one or more whitespace characters, False otherwise. 
    """
    return PATBOOK.is_match('is-blank', s)

def has_ltws(s: str) -> bool:
    """
    Returns True if the string consists leading or trailing whitespace characters, False otherwise. 
    """
    return PATBOOK.is_match('has-whitespace-left', s) or PATBOOK.is_match('has-whitespace-right', s)


def is_empty(s: str) -> bool:
    """
    Returns True if the string is equal to the empty string (''), True otherwise. 

    Obviously this function is quite trivial.  The point of having it is to allow us to profile for 
    this criterion along with all the other criteria.  See package notes for a more detailed 
    explanation.
    """
    if isinstance(s, str):
        return s == '' 
    raise TypeError("invalid input - not a string")

def is_alpha(s: str) -> bool:
    """
    Returns True if the string consists of one or more alphabetical characters, True otherwise. 
    In other words, equivalent to `str.isalpha()`.
    """
    return PATBOOK.is_match('is-alpha', s)

def is_integer_like(s: str) -> bool:
    return PATBOOK.is_match('is-integer-like', s)

def is_alphanumeric(s: str) -> bool:
    return PATBOOK.is_match('is-alphanumeric', s)


def has_upper(s: str) -> bool:
    """
    Returns True if the string consists of one or more upper case characters, True otherwise. 
    """
    if isinstance(s, str):
        return len(s) > 0 and not s.islower()
    raise TypeError("invalid input - not a string")

def has_lower(s: str) -> bool:
    """
    Returns True if the string consists of one or more lower case characters, True otherwise. 
    """
    if isinstance(s, str):
        return len(s) > 0 and not s.isupper()
    raise TypeError("invalid input - not a string")

def has_non(function: Callable) -> Callable:
    """
    A convenient operator that takes a function (presumed to have the same signature as all of
    the other functions in this section), and returns the logical "converse" - that is, a function 
    which returns True if any part of the input string fails to return True on the given function.

    For example, if we had a function `is_greek` which returns True is a string consists entirely
    of Greek cheracters - then `has_non(is_greek)` would return a callable which returns True if the
    given string contains any non-Greek characters.

    Note the function thus produced may be quite inefficient.  But in a pinch it can be useful to
    whip out "converse" forms of validating functions in this way.
    """
    def wrapped(string: str) -> bool:
        if isinstance(string, str):
            return any(not function(_) for _ in string) 
        raise ValueError("invalid input - not a string")
    return wrapped


def basic_shape(string: str) -> str:
    """
    Looks at a string and tries to determine it's basic "shape" for downstream processing.
    As the function name implies these assignment names very basic, but workable enough (for now).
    """
    if not isinstance(string,str):
        return None
    if len(string) == 0:
        return 'empty'
    if is_blank(string):
        return 'blank'
    if has_ltws(string):
        return 'malformed'
    if ' ' in string:
        return 'multiword'
    if is_delim(string,'-'):
        return 'dashy'
    if '-' in string: # contains '--' or leading/trailing '-'
        return 'malformed'
    return 'plain'

_wordpat = re.compile('\S+')
def extract_words(string: str) -> Iterator[str]: 
    yield from _wordpat.findall(string) 



def find_occurrence(string: str, sub: str, position: int, start: Optional[int] = None, end: Optional[int] = None) -> int:
    """
    Similar to `str.find`, but finds the offset of the `position-th` occurrence of `sub` in `string`. 
    If it can't be found, returns -1.
    """
    if len(sub) == 0:
        return 0
    marker: int = 0
    curpos: int = start if start is not None else 0
    if end is None:
        end = len(string)
    while marker <= position and curpos <= len(string): 
        j = string.find(sub, curpos)
        if j < 0 or marker == position:
            return j
        curpos = j + len(sub)
        marker += 1
    # Theoretically we should never get here, but if we do ...
    raise RuntimeError("invalid state") 

def find_line_occurrence(text: str, position: int, separator: str = "\n") -> Optional[Tuple[int,int]]:
    if position < 0:
        raise ValueError("invalid usage - position must be > 0") 
    if position == 0:
        j = text.find(separator)
        if j < 0:
            return None
        return (0, j)
    j0 = find_occurrence(text, separator, position)
    if j0 < 0:
        return None
    # Note that j1 can possible be -1 
    j1 = find_occurrence(text, separator, position-1)
    return (j0, j1)

