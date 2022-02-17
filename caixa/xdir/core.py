import os
import re
import pickle
from dataclasses import dataclass
from typing import List, Iterator, Optional, Any
import ioany

@dataclass
class ItemPat:
    label: str
    ext: str

    # TODO: memoize this regex construction. 
    # Definitely should not be recompiling it for every search!
    @property
    def _regex(self) -> re.Pattern: 
        return re.compile(f"{self.label}-(\S+)\.{self.ext}")

    def match(self, subpath: str) -> Optional[re.Match]: 
        return self._regex.match(subpath)

    def offset(self, subpath: str) -> Optional[int]:
        """
        Returns the `offset` component of the given `subpath` if valid (that is, if it matches 
        the derived internal pattern provided by `self._regex()`), or None otherwise.
        """
        m = self.match(subpath)
        return int(m.group(1)) if m else None


@dataclass
class ItemAttr:
    offset: int
    subpath: str


class XDir:
    """An object representing a directory in a POSIX-like file system."""

    def __init__(self, path: str, vivify: bool = False, verify: bool = True):
        self._path = path
        if vivify:
            self.vivify()
        else:
            self.verify()
        self._build()

    def _build(self) -> None:
        """
        A stub method provided for extension classes that wish to perform any
        attention build steps (after the constructor does its job).

        That is, a quick hack that allows us to modify what happens during the
        construction phase (without messing with the details of doing a proper 
        override of the constructor method itself).
        """
        pass

    @property
    def path(self) -> str:
        return self._path

    def __str__(self) -> str:
        return f"XDir('{self.path}')"

    def verify(self) -> None:
        if not os.path.isdir(self._path):
            raise ValueError(f"cannot verify directory path '{self._path}'")

    def vivify(self):
        if not os.path.isdir(self._path):
            os.mkdir(self._path)

    @property
    def basename(self) -> str:
        return os.path.basename(self.path) 

    @property
    def is_active(self) -> bool:
        return os.path.isdir(self.path)

    def assert_active(self):
        if not self.is_active:
            lcname = self.name.lower()
            raise RuntimeError(f"invalid usage - {lcname} inactive")


    def walk(self, **kwargs) -> Iterator[tuple]:
        top = self.path
        if os.path.isdir(top):
            return os.walk(top, **kwargs)
        else:
            raise RuntimeError(f"cannot traverse - toplevel path '{top}' not a directory")

    def get_dirs(self, sort: bool = True) -> List[str]:
        root, dirs, files = next(self.walk())
        if sort:
            dirs = sorted(dirs)
        return dirs

    def get_files(self, sort: bool = True) -> List[str]:
        root, dirs, files = next(self.walk())
        if sort:
            files = sorted(files)
        return files

    def get_all(self) -> List[str]:
        root, dirs, files = next(self.walk())
        return dirs + files

    def fullpath(self, subpath: str) -> str:
        return os.path.join(self.path, subpath)

    def exists(self, subpath: str) -> bool:
        """
        Tests whether an object exists under the given path.
        Returns True for broken symbolic links.
        """
        path = self.fullpath(subpath)
        return os.path.lexists(path)

    def is_dir(self, subpath : str) -> bool:
        path = self.fullpath(subpath)
        return os.path.isdir(path)

    def is_file(self, subpath : str) -> bool:
        path = self.fullpath(subpath)
        return os.path.isfile(path)

    def is_link(self, subpath : str) -> bool:
        path = self.fullpath(subpath)
        return os.path.islink(path)

    #
    # subdir stuff
    #

    def subdir(
            self, 
            dirname: str, 
            vivify: bool = False,
            strict: bool = False) -> Optional['XDir']: 
        # print(f"XDIR.subdir: dirname = {dirname}, vivify = {vivify}")
        fullpath = self.fullpath(dirname)
        if os.path.isdir(fullpath):
            return XDir(fullpath)
        if strict:
            raise RuntimeError(f"invalid state - couldn't find subdir '{dirname}' under expected location")
        if vivify:
            if os.path.exists(fullpath):
                raise ValueError(f"can't vivify subdir '{dirname}' under {self} - a non-directory object already exists at that location")
            os.mkdir(fullpath)
            return XDir(fullpath)
        # If we get here it means we didn't find the subdir under the expected location.
        # So we return None and let the calling context decide what to do about it.
        return None

    #
    # Item recognition
    #

    def find_items(self, label: str, ext: str) -> Iterator[ItemAttr]:
        itempat = ItemPat(label, ext)
        for subpath in self.get_files():
            offset = itempat.offset(subpath)
            if offset is not None:
                yield ItemAttr(offset, subpath)

    def item_path(self, label: str, ext: str, position: int) -> str:
        if position not in range (0,1000000):
            raise ValueError(f"invalid position '{position}'")
        fmtpos = "%.6d" % position
        return f"{label}-{fmtpos}.{ext}"


    #
    # The next 3 methods are basically congruent (up to the slurp method).
    #

    def load_json(self, subpath: str) -> object:
        path = self.fullpath(subpath)
        if self.exists(path):
            return ioany.load_json(path)
        raise ValueError(f"can't find JSON file at path = '{path}'")

    def save_json(self, subpath: str, obj: Any, sort_keys: bool = True, indent: int = 4):
        path = self.fullpath(subpath)
        ioany.save_json(path, obj, sort_keys, indent)

    def load_yaml(self, subpath: str) -> object:
        path = self.fullpath(subpath)
        if self.exists(path):
            return ioany.load_yaml(path)
        raise ValueError(f"can't find YAML file at path = '{path}'")

    def load_any(self, subpath: str) -> object:
        """
        Loads the struct at 'subpath', infers filetype (yaml, json) from path extension.
        """
        path = self.fullpath(subpath)
        return ioany.load_path(path)

    def save_recs(self, subpath: str, stream: Iterator[dict]):
        path = self.fullpath(subpath)
        return ioany.save_recs(path, stream)

    def slurp_csv(self, subpath: str) -> List[dict]:
        path = self.fullpath(subpath)
        if self.exists(path):
            return ioany.slurp_csv(path)
        raise ValueError(f"can't find CSV file at path = '{path}'")

    #
    # Pickling
    #

    def load_pickle(self, subpath: str) -> Any:
        fullpath = self.fullpath(subpath)
        with open(fullpath,"rb") as f:
            return pickle.load(f)

    def save_pickle(self, subpath: str, data: Any) -> None:
        fullpath = self.fullpath(subpath)
        with open(fullpath,"wb") as f:
            pickle.dump(data, f)

    #
    # Block-oriented pickling
    #


    def block_path(self, label: str, position: int) -> str:
        return self.item_path(label, 'pickle', position)

    def load_block(self, label: str, position: int) -> Any:
        subpath = self.block_path(label, position)
        return self.load_pickle(subpath)

    def save_block(self, label: str, position: int, block: Any) -> None:
        subpath = self.block_path(label, position)
        self.save_pickle(subpath, block)

    def read_blocks(self, label: str) -> Iterator[list]:
        items = self.find_items(label, 'pickle')
        for item in items:
            yield self.load_pickle(item.subpath)


