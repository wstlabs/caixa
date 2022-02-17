from typing import List, Tuple, Dict, Iterator, Any

def slice_dict(r: dict, keys: List[str], strict = True) -> dict: 
    d = {}
    for k in keys:
        if strict and k not in r:
            raise ValueError("slice key '{k}' not in target dict")
        d[k] = r.get(k)
    return d

def slice_recs(recs: Iterator[dict], keys: List[str], strict = True) -> Iterator[dict]:
    return (slice_dict(r, keys, strict) for r in recs)


#
# dict2kwstr and its supporting functions
#

def _any2str(x: Any) -> str:
    """Simple string casting for the purpose of our dict2argterms function."""
    if x is None:
        return 'None'
    if isinstance(x, str):
        return "'" + str(x) + "'" 
    return str(x)

def _kv2str(pair: Tuple[str, Any]) -> str:
    key, value = pair
    return f"{key}={_any2str(value)}"

def dict2argterms(d: Dict[str, Any]) -> Iterator[str]:
    """Given a dict, yields a sequence of properly stringified key-value terms that are 
    believed to be compatible with the usual presentation of kwarg dicts as strings.
    Can also be used for "pretty" representations of dicts in other contexts.
    So for example:

        >>> d = {'foo': 'bar', 'ook': None, 'this': 2}
        >>> ", ".join(dict2argterms(d))
        "foo='bar', ook=None, this=2"

    Note that we naively assume that the given `dict` is essentialy "kwarg-like", 
    (for example, that every key is a string, and contains no spaces or punctuation, etc).
    If not then you'll get garbage output."""
    return (_kv2str(kv) for kv in d.items())

def dict2pretty(d: Dict[str, Any]) -> str: 
    """Returns a "pretty" representation of a dict, believed to be compatible with the
    usual presentation of kwarg dicts.  For example:

        >>> d = {'foo': 'bar', 'ook': None, 'this': 2}
        >>> dict2pretty(d))
        "foo='bar', ook=None, this=2"

    As with dict2argterms, we assume that our given `dict` struct is essentially "kwarg-like"
    If not then you'll get garbage output."""
    return ", ".join(dict2argterms(d))

