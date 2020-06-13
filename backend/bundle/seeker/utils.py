import abc
import re

from typing import Mapping, Any, Callable, Union

from .pycompat import ABC, string_types, collections_abc


def _check_methods(C, *methods):
    mro = C.__mro__
    for method in methods:
        for B in mro:
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True


class WritableStream(ABC):
    @abc.abstractmethod
    def write(self, s):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is WritableStream:
            return _check_methods(C, 'write')
        return NotImplemented


file_reading_errors = (
    IOError,
    OSError,
    ValueError  # IronPython weirdness.
)


def shitcode(s):
    return ''.join(
        (c if (0 < ord(c) < 256) else '?') for c in s
    )


def get_repr_function(item: Any, custom_repr: Mapping[Union[Callable, type], Callable]) -> Callable:
    """
    get default representation function `repr` or custom representation function
    @param item: the item
    @param custom_repr: custom representation function mappings
    @return: representation function for the item
    """
    for condition, action in custom_repr:
        if isinstance(condition, type):
            condition = lambda x, y=condition: isinstance(x, y)
        if condition(item):
            return action
    return repr


DEFAULT_REPR_RE = re.compile(r' at 0x[a-f0-9A-F]{4,}')


def normalize_repr(item_repr):
    """
    Remove memory address (0x...) from a default python repr
    @param item_repr: the representation string of an item
    @return: normalized representation string of the item
    @deprecated: since the beginning
    """
    return DEFAULT_REPR_RE.sub('', item_repr)


def get_shortish_repr(item: Any,
                      custom_repr: Mapping[Union[Callable, type], Callable] = (),
                      max_length: int = None):

    repr_function: Callable = get_repr_function(item, custom_repr)
    try:
        r: str = repr_function(item)
    except Exception:
        r = 'REPR FAILED'
    r = r.replace('\r', '').replace('\n', '')
    if max_length:
        r = truncate(r, max_length)
    return r


def truncate(string, max_length):
    if (max_length is None) or (len(string) <= max_length):
        return string
    else:
        left = (max_length - 3) // 2
        right = max_length - 3 - left
        return u'{}...{}'.format(string[:left], string[-right:])


def ensure_tuple(x):
    if isinstance(x, collections_abc.Iterable) and \
                                               not isinstance(x, string_types):
        return tuple(x)
    else:
        return x,
