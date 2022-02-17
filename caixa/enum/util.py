from enum import Enum
from typing import Union

def enum2str(item: Union[Enum, str]) -> str:
    if item is None:
        return None
    if isinstance(item, Enum):
        return "" + str(item.value)
    if isinstance(item, str):
        return item
    raise TypeError(f"invalid item instance - can't deal with type = {type(item)}")


