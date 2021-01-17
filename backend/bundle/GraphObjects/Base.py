from __future__ import annotations
from abc import ABCMeta
from typing import Union, Iterable, Mapping, Type, MutableMapping, List, Callable, TypeVar, Generic, Set, Optional, \
    Generator
import json
import logging

from .Errors import InvalidStyleCollectionError, InvalidClassCollectionError, InvalidIdentityError


class Comparable(metaclass=ABCMeta):
    """
    Comparable interface allows you compare objects with their identity.
    """
    _PREFIX = ''
    _comparable_counter = 0

    def _get_id_string(self) -> str:
        type(self)._comparable_counter += 1
        return f'{self._PREFIX}_{type(self)._comparable_counter}'

    @staticmethod
    def identity_validator(identity: Union[str, int]) -> bool:
        return identity is not None

    def __init__(self, identity: Union[int, str], name=None):
        """
        Identity interface. Subclass should pass in an identity that should be comparable
        But it is restricted to `int` and `str` for now.
        @param identity: unique id for this object
        @param name: displayed name for this object
        """
        # TODO read SUID if id is not present.
        # TODO think of an naming convention for id
        if not self.identity_validator(identity):
            raise InvalidIdentityError
        self.identity: str = identity
        self.name: str = name if name else self._PREFIX + str(identity)
        self.cy_id: str = self._get_id_string()
        self._hash_cache = None

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.identity == other.identity
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self._hash_cache is None:
            self._hash_cache = hash((type(self), self.identity))
        return self._hash_cache

    def __gt__(self, other: Comparable):
        if not isinstance(other, Comparable):
            raise ValueError('Cannot compare %s with %s' % (self, other))
        return self.identity > other.identity

    def __lt__(self, other: Comparable):
        return not self.__gt__(other)

    def __ge__(self, other: Comparable):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other: Comparable):
        return self.__lt__(other) or self.__eq__(other)


class HasProperty(metaclass=ABCMeta):
    """
    Property interface allows you to manage defined property and access them through subscript;
    """

    def __init__(self):
        """
        create a property interface
        """
        self.properties: MutableMapping = {}

    def update_properties(self, properties: Mapping):
        self.properties.update(properties)

    def __getitem__(self, item):
        """
        get property
        @param item:
        @return:
        """
        return self.properties[item]

    def __setitem__(self, key, value):
        """
        set a property with some value
        @param key:
        @param value:
        """
        self.properties[key] = value

    def __contains__(self, item):
        """
        Check whether this object has certain property
        @param item:
        @return boolean value indicating whether the property is in this object
        """
        return item in self.properties

    def __iter__(self):
        """
        loop through all the properties
        @return:
        """
        for key, value in self.properties:
            yield key, value

    def __len__(self):
        """
        @return: the number of properties of this object
        """
        return len(self.properties)


class Stylable(metaclass=ABCMeta):
    default_styles = []
    default_classes = []

    @staticmethod
    def is_valid_graph_styles(styles: Iterable[Mapping]) -> bool:
        if isinstance(styles, Iterable):
            for element in styles:
                if not isinstance(element, Mapping) or 'selector' not in element or 'style' not in element:
                    return False
            return True
        return False

    @staticmethod
    def is_valid_graph_classes(classes: Iterable[str]) -> bool:
        return isinstance(classes, Iterable) and all(isinstance(element, str) for element in classes)

    def __init__(self, styles: Union[str, Iterable[Mapping]], classes: Union[str, Iterable[str]],
                 add_default_styles: bool = False,
                 add_default_classes: bool = True,
                 style_validator: Callable = None,
                 class_validator: Callable = None):
        """
        interface that helps managing the state of an element
        @param styles:
        @param classes:
        """

        self.styles: List[MutableMapping[str, str]] = []
        self.classes = []

        if isinstance(styles, str):
            try:
                styles = json.loads(styles)
            except Exception as e:
                logging.exception('Unknown Exception')
                raise InvalidStyleCollectionError(f'Cannot parse style string for {type(self)} - {e}'
                                                  f'(style literal: {styles}).')

        if isinstance(classes, str):
            try:
                classes = json.loads(classes)
            except Exception as e:
                raise InvalidClassCollectionError(f'Cannot parse class string for {type(self)} - {e}'
                                                  f'(class literal: {classes}).')

        if style_validator is None:
            style_validator = self.is_valid_graph_styles

        if class_validator is None:
            class_validator = self.is_valid_graph_classes

        if style_validator(styles):
            self.styles.extend(styles)
            if add_default_styles:
                self.styles.extend(self.default_styles)
        else:
            raise InvalidStyleCollectionError(f'Cannot init {type(self)} due to graph style format error '
                                              f'(styles: {styles}).')

        if class_validator(classes):
            self.classes.extend(classes)
            if add_default_classes:
                self.classes.extend(self.default_classes)
        else:
            raise InvalidClassCollectionError(f'Cannot init {type(self)} due to graph class format error '
                                              f'(classes: {classes}).')


_T = TypeVar('_T', bound=Comparable)


class ElementSet(Generic[_T]):
    def __init__(self, elements: Iterable[_T], element_type: Type[_T]):
        """
        Element set base class
        @param elements:
        @param element_type:
        """
        self.elements: Set[_T] = set()
        self.element_type: Type[_T] = element_type
        if isinstance(elements, Iterable) and all(isinstance(element, self.element_type) for element in elements):
            self.elements.update(elements)
        else:
            raise KeyError('elements are not all %s type' % self.element_type)

    def _rm_element(self, element):
        if isinstance(element, self.element_type) and element in self.elements:
            self.elements.remove(element)

    def is_empty(self):
        return len(self.elements) == 0

    def __len__(self):
        """
        return the number of elements in this set
        @return:
        """
        return len(self.elements)

    def __getitem__(self, identity: str) -> Optional[_T]:
        """
        use subscript [] to get item
        @param identity:
        @return:
        """
        for element in self.elements:
            if element.identity == identity:
                return element

        return None

    def __iter__(self) -> Generator[_T, None, None]:
        """
        iterator that goes through the elements in the set
        @return:
        """
        for element in self.elements:
            yield element

    def __contains__(self, item: Union[str, _T]) -> bool:
        """
        whether this set contains a given item
        @param item:
        @return:
        """
        if isinstance(item, self.element_type):
            return item in self.elements
        if isinstance(item, str):
            # TODO what about searches for names?
            return any(element.identity == item for element in self.elements)
        return False

    def __str__(self) -> str:
        return str(self.elements)

    def __repr__(self) -> str:
        return self.__str__()
