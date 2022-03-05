import re
import argparse
from copy import deepcopy
from gettext import gettext
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Any
from ..util.string import find_not

"""
Provides the class ArgMap, which deals with a somewhat obscure situation in argument
parsing that I have run into more than once.

It concerns the case when you have one tool somehow embedded in the other, and you'd like 
separate their argument sequences (with a reasonable degree of assurance) such that the 
parsing of these sequences can be done independently.

As an example, say you have tools `foo` and `bar`, and for your use case you will have 
their sequences catenated at the command like, like this:

    foo <foo-args> bar <bar-args>

The class ArgMap provides a static method that finds the appropriate spot in the argument 
sequence at which to partition between the two calling signatures.  It returns this value 
inside an object of class ArgSpec, which also stores an error string in case it was unable 
to parse.  If it is unable to parse, it sets the index value to -1 (in accord with the  
pattern for many common utilities that find certain patterns in strings and sequences).

Sample usage goes like this:

    >> argspec = ArgMap.resolve("foo --verbose --delay=5 bar --infile=data.csv --rowmax=1000")
    >> argspec.index
    3

We get the value 3 corresponding to the fact that the `foo` argument eats up the first 3 terms 
in the argument sequence (including the command `foo` itself).  The `resolve` method will do its 
best to make sense of different presentations of keyword-value pairs (which can appear with or
without the equal sign).  So if we feed the sequence:

    >> argspec = ArgMap.resolve("foo --verbose --delay 5 bar --infile=data.csv --rowmax=1000")
    >> argpec.index
    4

It now splits at position 4.  
"""




@dataclass
class ArgMap:
    argv: List[str]
    index: int 
    failmsg: Optional[str]

    @classmethod
    def ingest(cls, argv: List[str]) -> 'ArgMap':
        _argv: List[str] = deepcopy(argv)
        return ArgMap(argv=_argv)


class ArgSpec:

    def __init__(self, rawspec: Dict[str,Optional[str]]) -> None: 
        assert_valid_rawspec(rawspec)
        self._raw = deepcopy(rawspec)
        self._val = rawspec2valence(self._raw)

    def __str__(self) -> str:
        name: str = self.__class__.__name__
        return f"{name}(mono='{self.mono}', pair='{self.pair}')"

    @property
    def mono(self) -> Optional[str]:
        return self._raw.get('mono')

    @property
    def pair(self) -> Optional[str]:
        return self._raw.get('pair')

    def valence(self, keyword: str) -> Optional[int]:
        return self._val.get(keyword)

    def resolve(self, argv: List[str]) -> ArgMap: 
        _argv = deepcopy(argv)
        index: int = 0
        print(f"resolve: argv = {_argv}")
        while index < len(_argv):
            term = _argv[index]
            print(f"term[{index}] = '{term}' ..")
            if not term.startswith('-'):
                return ArgMap(_argv, index, None) 
            kwspec = KwargSpec.ingest(term)
            print(f"term[{index}] = '{term}' : {kwspec}")
            if not kwspec.status:
                return ArgMap(_argv, -1, f"malformed term '{term}' at position {index}")
            # If the status check passes, we're guarnteed to have at least a keyword term
            _valence = self.valence(kwspec.keyword)
            print(f"term[{index}] = '{term}' : keyword = '{kwspec.keyword}', _valence = {_valence}")
            if _valence is None:
                return ArgMap(_argv, -1, f"unrecognized term '{term}' at position {index}")
            if _valence == 0: 
                if kwspec.value is not None:
                    return ArgMap(_argv, -1, f"unexpected value for soliton keyword '{term}' at position {index}")
                index += 1
            elif _valence == 1: 
                if kwspec.value is None:
                    if index + 1 >= len(_argv):
                        return ArgMap(_argv, -1, f"expected value for paired keyword '{term}' at position {index}")
                    next_term = _argv[index + 1]
                    if next_term.startswith('-'):
                        return ArgMap(_argv, -1, f"expected value for paired keyword '{term}' at position {index}")
                    else:
                        index += 2
                else:
                    index += 1
            else:
                # Theoretically this should never happen
                return ArgMap(_argv, -1, f"invalid state after '{term}' at position {index}")
        return ArgMap(_argv, index, None) 


def assert_valid_rawspec_label(label: str) -> None:
   if label not in ('mono','pair'):
       raise ValueError(f"invalid rawspec label '{label}'")


def assert_valid_rawspec(rawspec: Dict[str,str]) -> None:
    for k in rawspec.keys():
        assert_valid_rawspec_label(k)

def label2valence(label: str) -> int:
    if label == 'mono':
        return 0
    if label == 'pair':
        return 1 
    raise ValueError("invalid rawspec label '{label}'")


@dataclass
class KwargSpec:
    keyword: Optional[str]
    value: Optional[str]
    failmsg: Optional[str]

    @property 
    def status(self) -> bool:
        return self.failmsg is None

    @classmethod
    def ingest(cls: type, term: str) -> 'KwargSpec': 
        return parse_kwarg_term(term)


def parse_kwarg_term(term: str) -> KwargSpec: 
    index: int = find_not(term, '-')
    if index < 1:
        return KwargSpec(keyword=None, value=None, failmsg="not dashy") 
    # residue = term[index:]
    index = term.find('=')
    if index < 0:
        return KwargSpec(keyword=term, value=None, failmsg=None)
    elif term.find('=',index+1) < 0:
        return KwargSpec(keyword=term[:index], value=term[index+1:], failmsg=None)
    else:
        return KwargSpec(keyword=None, value=None, failmsg="too many equal signs") 


def rawspec2valence(rawspec: Dict[str,str]) -> Dict[str,int]:
    _val: Dict[str,int] = {}
    label: str
    terms: str
    for (label,terms) in rawspec.items():
        if label not in ('mono','pair'):
            raise ValueError(f"invalid rawspec - bad label '{label}'")
        _valence: int = label2valence(label)
        _terms: List[str] = [t for t in terms.split(',') if len(t)]
        for term in _terms:
            if term in _val:
                raise ValueError(f"invalid term list for label '{label}' - duplicate instance of term '{term}'")
            _val[term] = _valence
    return _val

        



"""
def splitargv(argv: List[str], spec: Dict[str,Any] = None) -> ArgMap: 
    raise RuntimeError("deprecated")


def splitargv_simple(argv: List[str]) -> ArgMap: 
    "Splits an argument vector into positional and keyword arguments."
    argv = deepcopy(argv)
    i = kwindex_simple(argv)
    if i is None:
        (posargs, kwargs) = (argv[:], [])
    else:
        (posargs, kwargs) = (argv[:i], argv[i:])
    return (posargs, kwargs)

def splitargv_fancy(argv: List[str], spec: Dict[str,Optional[str]]) -> Tuple[List[str],List[str]]:
    raise RuntimeError("not implemented")


def first_nonkwarg(argv: List[str]) -> Optional[str]: 
    "Given a list of strings :argv, returns the first element (if it is a non-kwarg), else None"
    if len(argv) > 0:
        if not argv[0].startswith('-'):
            return argv[0]
    return None

def kwindex_simple(argv: List[str]) -> Optional[int]:
    "Returns the array position of the first keyword-like argument (that is, the
    first argument that starts with a dash) if found, else None."
    i = 0
    while i < len(argv) and not argv[i].startswith('-'):
        i += 1
    return i if i < len(argv) else None
"""


