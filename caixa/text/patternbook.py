import re
from typing import Dict, Optional


class PatternBook: 
   
    def __init__(self, lookup: Dict[str,re.Pattern]):
        self.lookup = lookup

    # def match(self, name: str, string: str, pos: int = None, endpos: int = None) -> re.Match:
    def match(self, name: str, string: str) -> Optional[re.Match]:
        if name in self.lookup:
            return self.lookup[name].match(string)
        else:
            raise ValueError(f"unknown pattern '{name}'")

    def is_match(self, name: str, string: str) -> bool: 
        return bool(self.match(name, string))

    #
    # The following methods provide a partial facade pattern to the underlying dict struct.
    #

    def __getitem__(self, name: str) -> object:
        return self.lookup.__getitem__(name)

    def __len__(self) -> int:
        return len(self.lookup)

    def __contains__(self, name: str) -> int:
        return name in self.lookup 


