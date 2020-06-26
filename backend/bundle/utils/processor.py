from copy import copy
from typing import Tuple, Mapping, List, Any, Iterable, MutableMapping, Optional
import json

from bundle.GraphObjects.Edge import Edge
from bundle.GraphObjects.Node import Node


def make_tuple(var) -> Tuple:
    return var,


class Processor:
    COLOR_PALETTE = ["#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C",
                     "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00",
                     "#CAB2D6", "#6A3D9A", "#FFFF99", ]

    ACCESSED_COLOR = "#B15928"
    ACCESSED_IDENTIFIER = ('global', '__accessed_variables')
    """
    Processor should return the state at that line if changes took place in the code
    if some variables are not changed, I will record it's value. If it's empty, the corresponding
    value will be set to none.
    """
    def __init__(self, variable_number_limit: int = 10):
        # TODO put the register work to recorder
        self.variable_number_limit = variable_number_limit
        self._no_limit = False
        self.variable_color_map: dict = {}
        self.result = []
        self.result_json = None

    def _no_limit_override(self, flag: bool) -> None:
        self._no_limit = flag

    def load_variables_and_create_color_map(self, variables: List[Tuple[str, str]]) -> None:
        if len(variables) > self.variable_number_limit and not self._no_limit:
            raise AssertionError('The number of variable input cannot exceed {}!'.format(self.variable_number_limit))

        self.create_color_map(variables)

    def create_color_map(self, variables: List[Tuple[str, str]]) -> None:
        for variable, color in zip(variables, self.COLOR_PALETTE):
            self.variable_color_map[variable] = color

    def get_result_json(self) -> Mapping:
        if not self.result_json:
            self.generate_result_json()
        return self.result_json

    def generate_result_json(self) -> None:
        self.result_json = json.dumps(self.result)

    def load_data(self, change_list: List[Mapping], variables: List[Tuple]) -> object:
        self.load_variables_and_create_color_map(variables=variables)

        # init the mapping with None values, indicating at the beginning of the program nothing is initialized
        record_mapping = {self.ACCESSED_IDENTIFIER: None}
        record_mapping.update(zip(variables, [None] * len(variables)))

        for mapping in change_list:
            self.result.append(self.generate_record_template(
                record_mapping=record_mapping,
                line=mapping['line'],
                variable_changes=mapping['variables'],
                accessed_variables=mapping['accessed']
            ))

        return self.result

    def generate_record_template(self,
                                 record_mapping: MutableMapping[Tuple[str, str], Any],
                                 line: int,
                                 variable_changes: Mapping[Tuple[str, str], Any],
                                 accessed_variables: List) -> Mapping:
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

        record_mapping = copy(record_mapping)

        if isinstance(variable_changes, Mapping):
            # only update the changes by looping through variable change list
            for key, value in variable_changes.items():
                # TODO use graph elements' parent class
                if isinstance(value, (Node, Edge)):
                    variable_value = {
                        'id': value.identity,
                        'color': self.variable_color_map[key]
                    }
                else:
                    variable_value = repr(value)

                record_mapping[key] = variable_value

        record_mapping[self.ACCESSED_IDENTIFIER] = self.resolve_accessed(accessed_variables=accessed_variables)

        return {'line': line, 'variables': record_mapping}

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
