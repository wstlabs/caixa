"""
Dead simple options management.

The key to keeping "options" management simple lies in recognizing that differs (crucially) from "configuration" management:
    
  - By definition, option settings should always be -optional- (so we do not need to keep track of 
    which option keys are required or not - only whether they are permitted or not).

  - Option values should ideally by very simple (boolean, strings, numerics) and in most cases should not 
    require validation (at least at the 'option-passing') level.  That said, values can be of any type -
    but if any validation or type checking is required (beyond that the types match exactly what is prent
    in the default options dict), then it needs to be done externally.

  - Option setting (and generation) happens in runtime -- most typically as an `options` dict passed to 
    some function.  So for the purpose of "option" management, we need not be concerned about locating and
    parsing config files.

Further, the scope will most likely be at module, class or instance level.  So this means we don't need to worry
about walking up class trees to find some default options dict.

So at least 90 percent of the time - this boils down to "carefully merging dicts".  

The most likely use case goes about like this: 

```
from caixa.options import resolve_options

DEFAULTOPTIONS = {'allow-snorkeling': True, 'rescue-after': 10} 

    # then somewhere in a module or class
    def rescue_person(self, instructor: str, options: Dict[str,any]): 
        niceopts = resolve_options(DEFAULTOPTIONS, options)
```

That's it, and most of the time, it should be all you need.

TODO: enforce type compliance on values.
"""

from copy import deepcopy
from typing import Dict, Any

def update_strict(targetdict: dict, otherdict: dict, forcedeep: bool = True) -> None: 

    """
    Like `dict.update()` except:
      - We require that every key in the :otherdict be present in the :targetdict we are copying into
      - Only keys of type `str` (and of non-zero-length) are allowed 
      - A `deepcopy` is performed on each target value (unless `forcedeep` evaluates to False)
    """ 
    for (k, v) in otherdict.items():
        assert_valid_option_key(k)
        if k not in targetdict:
            raise ValueError(f"invalid option key '{k}' - not recognized") 
        targetdict[k] = deepcopy(v) if forcedeep else v

def assert_valid_option_key(k: str) -> None:
    if not isinstance(k, str):
        raise ValueError(f"invalid option key '{k}' - must be of type str") 
    if len(k) == 0:
        raise ValueError(f"invalid option key '{k}' - cannot be the empty string") 

def resolve_options(default_options: Dict[str,Any], update_options: Dict[str,Any]) -> Dict[str,Any]:
    """
    Returns a new options dict, with the :default_options and :update_options dicts safely merged.
    """
    if update_options is None:
        update_options = {}
    newoptions = deepcopy(default_options)
    update_strict(newoptions, update_options)
    return newoptions 

