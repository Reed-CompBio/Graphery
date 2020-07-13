"""Python 2/3 compatibility"""

import abc
import os
import inspect
import sys
import datetime as datetime_module

PY3 = (sys.version_info[0] == 3)
PY2 = not PY3

if hasattr(abc, 'ABC'):
    ABC = abc.ABC
else:
    class ABC(object):
        """Helper class that provides a standard way to create an ABC using
        inheritance.
        """
        __metaclass__ = abc.ABCMeta
        __slots__ = ()


if hasattr(os, 'PathLike'):
    PathLike = os.PathLike
else:
    class PathLike(ABC):
        """Abstract base class for implementing the file system path protocol."""

        @abc.abstractmethod
        def __fspath__(self):
            """Return the file system path representation of the object."""
            raise NotImplementedError

        @classmethod
        def __subclasshook__(cls, subclass):
            return (
                hasattr(subclass, '__fspath__') or
                # Make a concession for older `pathlib` versions:g
                (hasattr(subclass, 'open') and
                 'path' in subclass.__name__.lower())
            )


try:
    iscoroutinefunction = inspect.iscoroutinefunction
except AttributeError:
    iscoroutinefunction = lambda whatever: False  # Lolz

try:
    isasyncgenfunction = inspect.isasyncgenfunction
except AttributeError:
    isasyncgenfunction = lambda whatever: False  # Lolz


if PY3:
    string_types = (str,)
    text_type = str
else:
    raise EnvironmentError('You must use python3')

if sys.version_info[:2] >= (3, 6):
    time_isoformat = datetime_module.time.isoformat
else:
    raise EnvironmentError('You must use python 3.6 or above')


def timedelta_format(timedelta):
    time = (datetime_module.datetime.min + timedelta).time()
    return time_isoformat(time, timespec='microseconds')


def timedelta_parse(s):
    hours, minutes, seconds, microseconds = map(
        int,
        s.replace('.', ':').split(':')
    )
    return datetime_module.timedelta(hours=hours, minutes=minutes,
                                     seconds=seconds,
                                     microseconds=microseconds)
