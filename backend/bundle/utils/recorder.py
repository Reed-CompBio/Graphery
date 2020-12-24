from __future__ import annotations

import json
from collections.abc import Mapping, Set
from collections import Counter
from numbers import Number
from random import randint
from typing import Any, List, MutableMapping, Sequence, Tuple, Deque, Union

from ..GraphObjects.Edge import Edge
from ..GraphObjects.Node import Node


IDENTIFIER_SEPARATOR = u'\u200b@'


def identifier_to_string(identifier: Sequence[str]) -> str:
    return IDENTIFIER_SEPARATOR.join(identifier)


def generate_hex() -> str:
    random_number = randint(0, 0xffffff)
    hex_number = str(hex(random_number))
    return '#' + hex_number[2:]


class Recorder:
    """
    The recoder is used to record variable changes in each step
    the format is a list containing dictionaries::

        [
            {
                'line': line,
                'variables': {
                    'identity': {
                        'type': 'some_type',
                        'color': 'some_color_hex',
                        'repr': 'some_repr',
                        'properties': {
                            'property_1': str or number,
                            ...
                        }
                    }
                },
                'accesses': [
                    {
                       'type': 'some_type',
                        'color': 'some_color_hex',
                        'repr': 'some_repr',
                        'properties': {
                            'property_1': str or number,
                            ...
                        }
                    }
                ],
                'order': ['identity1', 'identity2', ...]
            },
            ...
        ]
    """
    _COLOR_PALETTE = ["#828282", "#B15928",  # reserved for inner variables and global access
                      "#A6CEE3", "#1F78B4", "#B2DF8A",
                      "#33A02C", "#FB9A99", "#E31A1C",
                      "#FDBF6F", "#FF7F00", "#CAB2D6",
                      "#6A3D9A", "#FFFF99"]
    _ACCESSED_IDENTIFIER = ('global', 'accessed var')
    _ACCESSED_IDENTIFIER_STRING = identifier_to_string(_ACCESSED_IDENTIFIER)

    _INNER_IDENTIFIER = ('', u'\u200b'.join('inner'))
    _INNER_IDENTIFIER_STRING = identifier_to_string(_INNER_IDENTIFIER)

    _SINGULAR_MAPPING = {
        Number: 'Number',
        str: 'String',
        Node: 'Node',
        Edge: 'Edge',
        type(None): 'None',
    }

    _CONTAINER_MAPPING = {
        List: 'List',
        Tuple: 'Tuple',
        Deque: 'Deque',
        Counter: 'Counter',
        Set: 'Set',  # which includes Set, set, KeyView(dict_keys), ValueView(dict_values), ItemView(dict_items),
        # frozenset, MutableSet
        Mapping: 'Mapping',  # which includes mappingproxy (not sure what that is), MutableMapping, dict
        Sequence: 'Sequence',  # which includes tuple, str, range, memoryview, MutableSequence, list, bytearray
    }

    _TYPE_MAPPING = {
        # simple individuals
        **_SINGULAR_MAPPING,
        # simple containers
        **_CONTAINER_MAPPING,
        # wildcard
        object: 'Object',
    }
    _INIT_TYPE_STRING = 'init'

    _GRAPH_OBJECT_TYPES = {'Node', 'Edge'}

    _TYPE_HEADER = 'type'
    _COLOR_HEADER = 'color'
    _REPR_HEADER = 'repr'
    _ID_HEADER = 'id'
    _PROPERTY_HEADER = 'properties'

    _LINE_HEADER = 'line'
    _VARIABLE_HEADER = 'variables'
    _ACCESS_HEADER = 'accesses'

    _BAD_REPR_STRING = 'BAD REPR FUNCTION'

    def __init__(self):
        self._changes: List[MutableMapping] = []
        # self.variables: Set[str] = set()
        self._color_mapping: MutableMapping = {}
        self._INNER_IDENTIFIER_STRING = self.register_variable(self._INNER_IDENTIFIER)
        self._ACCESSED_IDENTIFIER_STRING = self.register_variable(self._ACCESSED_IDENTIFIER)

    def assign_color(self, identifier_string: str) -> None:
        if identifier_string not in self._color_mapping:
            if len(self._color_mapping) < len(self._COLOR_PALETTE):
                color = self._COLOR_PALETTE[len(self._color_mapping)]
            else:
                color = generate_hex()
                while color in self._color_mapping.values():
                    color = generate_hex()
            self._color_mapping[identifier_string] = color

    def register_variable(self, identifier: Sequence[str]) -> str:
        """Register a variable

        a variable is identified by a identifier, which is
        a tuple of two strings. The first strings is the
        name of the place, ie functions etc., in which the
        variable is created. The second string is the variable
        name.
        @param identifier:
        @return:
        """
        identifier_string = identifier_to_string(identifier)
        self.assign_color(identifier_string)
        return identifier_string

    # TODO test this
    def add_record(self, line_no: int = -1) -> None:
        """
        add a record to the change list
        name clarification:
                            - @keyword variables: means variable changes
                            - @keyword accesses: means access changes
        @param line_no: the line number
        """
        self._changes.append({self._LINE_HEADER: line_no, self._VARIABLE_HEADER: None, self._ACCESS_HEADER: None})

    def get_last_record(self) -> MutableMapping:
        """
        get the last record
        @return: the last record
        """
        return self._changes[-1]

    def get_previous_record(self) -> MutableMapping:
        """Get the second last record in the record list

        In general cases, the first input line may not be
        empty, so `self.changes[-2]` will result in
        IndexError. In this case, we use `self.changes[-1]`
        """
        # this should not be a problem in official use, since the first line in the main function
        # ie. `def main()`: has no variables.
        return self._changes[-2] if len(self._changes) > 1 else self._changes[-1]

    def get_last_vc(self) -> MutableMapping:
        """get the last variable change dict

        @return: variables dict in the last record
        """
        last_variable_change = self.get_last_record()[self._VARIABLE_HEADER]
        if last_variable_change is None:
            last_variable_change = self.get_last_record()[self._VARIABLE_HEADER] = {}

        return last_variable_change

    def get_previous_vc(self) -> MutableMapping:
        """Get the second last dict in the record list"""
        previous_variable_change = self.get_previous_record()[self._VARIABLE_HEADER]
        if previous_variable_change is None:
            previous_variable_change = self.get_previous_record()[self._VARIABLE_HEADER] = {}

        return previous_variable_change

    def get_last_ac(self) -> List:
        """
        get the access list from the last record 
        @return: accesses list in the last record
        """
        if self.get_last_record()['accesses'] is None:
            self.get_last_record()['accesses'] = []

        return self.get_last_record()['accesses']

    def custom_repr(self, variable_state: Any, variable_type: str) -> Any:
        try:
            repr_result = repr(variable_state)
        except Exception:
            repr_result = self._BAD_REPR_STRING

        return repr_result

    def process_variable_state(self, identifier_string: str, variable_state: Any) -> MutableMapping:
        state_mapping: MutableMapping = {}

        for type_candidate, type_string in self._TYPE_MAPPING.items():
            if isinstance(variable_state, type_candidate):
                state_mapping[self._TYPE_HEADER] = type_string
                break

        if self._TYPE_HEADER not in state_mapping:
            # which should never happen
            raise  # TODO define exception

        state_mapping[self._REPR_HEADER] = self.custom_repr(variable_state, state_mapping[self._TYPE_HEADER])

        if state_mapping[self._TYPE_HEADER] in self._GRAPH_OBJECT_TYPES:
            variable_state: Union[Node, Edge]
            state_mapping[self._PROPERTY_HEADER] = self.custom_repr(variable_state.properties,
                                                                    self._TYPE_MAPPING[Mapping])
            state_mapping[self._COLOR_HEADER] = self._color_mapping[identifier_string]
            state_mapping[self._ID_HEADER] = variable_state.identity

        return state_mapping

    def add_vc_to_last_record(self, variable_identifier_string: str, variable_state: Any) -> None:
        """
        add a variable change to the last record
        @param variable_identifier_string: (name_space, variable_name)
        @param variable_state: the variable state
        @return: None
        """
        # if isinstance(variable_change, Tuple):
        self.get_last_vc()[variable_identifier_string] = self.process_variable_state(variable_identifier_string,
                                                                                     variable_state)

    def add_vc_to_previous_record(self, variable_identifier_string: str, variable_state: Any) -> None:
        """Add variable change to previous (second last if possible) record.

        When the variable is created/changed in line a,
        the tracer evaluate it in line a+1. So, this function
        is created to deal with this offset
        @param variable_identifier_string:
        @param variable_state:
        @return:
        """
        # if isinstance(variable_change, Tuple) and len(self.changes) > 1:
        self.get_previous_vc()[variable_identifier_string] = self.process_variable_state(variable_identifier_string,
                                                                                         variable_state)

    def add_ac_to_last_record(self, access_change: Any) -> None:
        """
        add an access change to the last record
        @param access_change: what's accessed
        @return: None
        """
        self.get_last_ac().append(self.process_variable_state(self._ACCESSED_IDENTIFIER_STRING, access_change))

    def get_change_list(self) -> List[MutableMapping]:
        temp = [
            {
                'line': 0,
                'variables': {
                    key: {
                        'type': self._INIT_TYPE_STRING,
                        'color': None,
                        'repr': None
                    }
                    for key, value in self._color_mapping.items()
                    if not (key == self._INNER_IDENTIFIER_STRING or key == self._ACCESSED_IDENTIFIER_STRING)
                },
                'accesses': None
            },
            *self._changes
        ]
        return temp

    def get_change_list_json(self) -> str:
        return json.dumps(self.get_change_list())

    def purge(self) -> None:
        """Empty previous recorded items"""
        self._changes: List[dict] = []
        # self.variables: Set[Tuple[str, str]] = set()
        self._color_mapping: MutableMapping = {}
