from typing import Any, Optional

def croplist(array: list[Any], depth: int = 3, maxlen: Optional[int] = None) -> str:
    """
    Returns an "edge-cropped" string representation of the given list :array with 
    the aim of giving you a quick portrait of the array's contents.  It assumes the
    use case of a very long list which would otherwise be too long to display on 
    a single line.

    For example, the list representing the set of primes between 100k and 110k
    (which has 1095 elements) would be presented like this:

        [100009, 100017, 100021 ... 109989, 109993, 109997]

    At present the only way to control the presentation is to supply the :depth
    parameter specifying the number of terms to emit on the left and right sides. 

    This design has some obvious shortcomings - for example, if you have some 
    elements with very long string elements within the chosen :depth, then it just
    spits them out as-is (and this effectively breaks the "cropping" mechanism).

    So a smarter rending approach is needed.  For many use cases however,
    the current approach can be fairly useful.
    """
    #
    # The `maxlen` parameter is just a placeholder for now.
    #
    if maxlen is not None:
        raise ValueError("explicit maxlen parameter not yet supported")
    if depth < 1:
        raise ValueError("invalid depth parameter = {depth}")
    if len(array) < 2 * depth:
        return str(array)
    crop_l = str(array[:depth])
    crop_r = str(array[-depth:])
    return crop_l[:-1] + " ... " + crop_r[1:] 

# for backward compatibility
list2cropped = croplist

