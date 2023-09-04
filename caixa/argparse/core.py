import argparse
from copy import deepcopy
from gettext import gettext
from typing import Optional

class Namespace(argparse.Namespace):
    pass

class ArgumentParser(argparse.ArgumentParser):
    """A monkey-patched version of argparse.ArgumentParser that overrides the default 
    error-handling mechanism.  Instead of calling sys.exit on errors, we re-route
    the error message to the hidden '_message' member of the argparse.Namespace 
    struct, which is always returned.  This allows us to provide fully custom 
    handling for all failure cases.

    (The same re-routing happens at the level of the parser object as well, but since 
    the Namespace object will always be available, that's the first place you should 
    look for it).  """

    def __init__(self, *args, **kwargs) -> None:
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self._message: Optional[str] = None

    def error(self, message: str): # -> None
        """Overrides the standard `error` method to assign the given :message to the 
        member `_message` of the parser instance.  In theory this will allow for fully
        customizable error handling."""
        self._message = message

    def parse_args(self, args=None, namespace=None): # -> argparse.Namespace
        """Overrides the standard `parse_args` method to re-route any parsing errors to
        a new `_message` member of the `argparse.Namespace` object, which is now always
        returned."""
        self._message = None
        response = self.parse_known_args(args, namespace)
        if self._message is not None:
            args = argparse.Namespace()
            args._message = deepcopy(self._message)
            return args
        # From this point it behaves exactly as the parse_args method (through Python 3.9),
        # except that we catch and re-route the error message (rather than do sys.exit).
        args, argv = response 
        args._message = None 
        if argv:
            msg = gettext('unrecognized arguments: %s')
            args._message = msg % ' '.join(argv)
        return args

    @classmethod
    def default_instance(cls) -> 'ArgumentParser':
        """An alternate constructor which returns a parser instance with the default --help  
        behavior overriden.  Instead of calling print_help and exiting, it attemps to parse
        the --help/-h flags like any other option.

        As a result, if the parse fails, the usual behavior of invoking the --help flag
        at the end of a complex argv sequence will of course not work.  But again, the idea
        of using this instance is that we'll be providing fully custom handling of all
        failure cases."""
        parser = cls(add_help=False)
        parser.add_argument("--help", action="store_true", help="show help")
        parser.add_argument("-h", action="store_true", help="show help")
        return parser

