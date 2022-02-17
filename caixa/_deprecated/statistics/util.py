from statistics import median_grouped
from collections import defaultdict
from functools import reduce

"""
DEPRECATED
Some stats helper classes in arrested development. 
Once we remember what it was we used them for, we'll get tidied up and better documented.
"""

def hist2median(histo):
    """The grouped median of an integer histogram."""
    return median_grouped(
        reduce(
           lambda x,y:x+y, [
              [k]*v for k,v in histo.items()
           ]
        )
    )


class TaggedHistogram: 

    def __init__(self) -> None:
        self.h: dict = {}

    def keys(self):
        return self.h.keys()

    def __getitem__(self,tag):
        return self.h[tag]

    def incr(self, tag, key) -> None:
        if tag not in self.h:
            self.h[tag] = defaultdict(int)
        self.h[tag][key] += 1

