from abc import ABCMeta, abstractmethod
from typing import Union


class Highlightable(metaclass=ABCMeta):
    @abstractmethod
    def highlight(self, color):
        """
        make this object highlighted
        @param color: the color of which this object should be highlighted
        @raise: NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def unhighlight(self, color):
        """
        unhighlight this object
        @param color: the color of which this object should be highlighted
        @raise: NotImplementedError
        """
        raise NotImplementedError


class Hashable(metaclass=ABCMeta):
    def __init__(self, identity: Union[int, str], name=None):
        """
        Identity interface. Subclass should pass in an identity that should be comparable
        But it is restricted to `int` and `str` for now.
        @param identity: unique id for this object
        @param name: displayed name for this object
        """
        self.identity = identity
        self.name = name

    def __eq__(self, other: 'Hashable'):
        if not isinstance(other, Hashable):
            return False
        return self.identity == other.identity

    def __ne__(self, other: 'Hashable'):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.identity)

    def __gt__(self, other: 'Hashable'):
        if not isinstance(other, Hashable):
            raise ValueError('Cannot compare %s with %s' % (self, other))
        return self.identity > other.identity

    def __lt__(self, other: 'Hashable'):
        return not self.__gt__(other)

    def __ge__(self, other: 'Hashable'):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other: 'Hashable'):
        return self.__lt__(other) or self.__eq__(other)


class HasProperty(metaclass=ABCMeta):
    def __init__(self):
        self.properties = {}

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value
