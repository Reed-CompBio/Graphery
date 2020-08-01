from copy import copy
from random import randint
from typing import Tuple, Mapping, List, Any, Iterable, MutableMapping, Optional, Set, Union
import json

from bundle.GraphObjects.Edge import Edge
from bundle.GraphObjects.Node import Node


def identifier_to_name(identifier: Tuple[str, str]) -> str:
    return '{}#{}'.format(*identifier)


class Processor:
    COLOR_PALETTE = ["#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C",
                     "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00",
                     "#CAB2D6", "#6A3D9A", "#FFFF99", ]

    ACCESSED_COLOR = "#B15928"
    ACCESSED_IDENTIFIER = ('global', 'accessed var')
    ACCESSED_ID_NAME = identifier_to_name(ACCESSED_IDENTIFIER)
    """
    Processor should return the state at that line if changes took place in the code
    if some variables are not changed, I will record it's value. If it's empty, the corresponding
    value will be set to none.
    """

    def __init__(self, variable_number_limit: int = 10):
        self.variable_number_limit = variable_number_limit
        self._no_limit = False
        self.variable_color_map: dict = {}
        self.result: List[MutableMapping] = []
        self.result_json: Optional[str] = None

    def _no_limit_override(self, flag: bool) -> None:
        self._no_limit = flag

    def load_variables_and_create_color_map(self, variables: Set[Tuple[str, str]]) -> None:
        if len(variables) > self.variable_number_limit and not self._no_limit:
            raise AssertionError('The number of variable input cannot exceed {}!'.format(self.variable_number_limit))

        self.create_color_map(variables)

    @staticmethod
    def generate_hex() -> str:
        random_number = randint(0, 16777215)
        hex_number = str(hex(random_number))
        return '#' + hex_number[2:]

    @staticmethod
    def generate_hex_list(number_of_hex: int, color_list: List[str]) -> List[str]:
        for i in range(number_of_hex):
            hex_color = Processor.generate_hex()
            while hex_color in color_list:
                hex_color = Processor.generate_hex()

            color_list.append(hex_color)
        return color_list

    def create_color_map(self, variables: Set[Tuple[str, str]]) -> None:
        diff = len(variables) - len(self.COLOR_PALETTE)
        if diff > 0:
            Processor.generate_hex_list(diff, self.COLOR_PALETTE)

        for variable, color in zip(variables, self.COLOR_PALETTE):
            self.variable_color_map[variable] = color

    def get_result_json(self) -> str:
        return self.result_json

    def generate_result_json(self) -> None:
        self.result_json = json.dumps(self.result)

    def load_data(self, change_list: List[Mapping], variables: Set[Tuple[str, str]]) -> object:
        self.load_variables_and_create_color_map(variables=variables)

        # init the mapping with None values, indicating at the beginning of the program nothing is initialized
        record_mapping: MutableMapping[str, Any] = {self.ACCESSED_ID_NAME: None}
        record_mapping.update(zip([identifier_to_name(var) for var in variables], [None] * len(variables)))

        init_mapping = copy(record_mapping)

        # append it in the first item of the list?

        for mapping in change_list:
            self.result.append(
                self.generate_record_template(
                    record_mapping=record_mapping,
                    line=mapping['line'],
                    variable_changes=mapping['variables'],
                    accessed_variables=mapping['accesses']
                ))

        # insert
        if self.result and self.result[0]['variables'] is None:
            self.result[0]['variables'] = init_mapping

        return self.result

    def generate_record_template(self,
                                 record_mapping: MutableMapping[str, Any],
                                 line: int,
                                 variable_changes: Mapping[Tuple[str, str], Any],
                                 accessed_variables: List) -> MutableMapping:
        """
        the result will be::

            [{
                'line': 1,
                'variables': {
                    'name1': 1,
                    'name2': {
                        'id': 1,
                        'color': '#123456'
                    },
                    '__accessed_variables': [{'id': 2, 'color': '#654321'}]
                },
                ...
            ]

        :param record_mapping:
        :param line:
        :param variable_changes:
        :param accessed_variables:
        :return:
        """

        if variable_changes is None and accessed_variables is None:
            return {'line': line, 'variables': None}

        if isinstance(variable_changes, Mapping):
            # only update the changes by looping through variable change list
            for key, value in variable_changes.items():
                record_mapping[identifier_to_name(key)] = self.resolve_variable(key, value)

        record_mapping[self.ACCESSED_ID_NAME] = self.resolve_accessed(accessed_variables=accessed_variables)

        # only save a copy of the dict or all the `variables` will point to one thing
        return {'line': line, 'variables': copy(record_mapping)}

    def resolve_variable(self, name: Tuple[str, str], value: Any) -> Union[str, Mapping]:
        representation = repr(value)
        # TODO use graph elements' parent class
        # TODO add `displayed` properties to var obj
        if isinstance(value, (Node, Edge)):
            # TODO create an interface here. Using str and dict is not a long-term solution
            variable_value = {
                'id': value.identity,
                'color': self.variable_color_map[name],
                'label': representation
            }
        else:
            variable_value = representation

        return variable_value

    @classmethod
    def resolve_accessed(cls, accessed_variables) -> Optional[List]:
        if isinstance(accessed_variables, Iterable):
            record = []
            for element in accessed_variables:
                if isinstance(element, (Node, Edge)):
                    variable_value = {
                        'id': element.identity,
                        'color': cls.ACCESSED_COLOR
                    }
                else:
                    variable_value = repr(element)
                record.append(variable_value)

            return record
        return None

    def purge(self):
        self.variable_color_map: dict = {}
        self.result = []
        self.result_json = None
