from typing import Tuple

from copy import copy
INDEX_PLACE_HOLDER = '___'


class ChangeList:
    def __init__(self):
        self.change_list = []

    def record(self, line_no: int, variables: dict = None, accesses: list = None):
        self.change_list.append({
            'line': line_no,
            'variables': variables,
            'accesses': accesses
        })
        return self

    @staticmethod
    def gen_record(line_no: int, variables: dict = None, accesses: list = None):
        return {
            'line': line_no,
            'variables': variables,
            'accesses': accesses
        }

    @staticmethod
    def replace_values_with_index(index: int, variable_dict: dict):
        variable_dict = copy(variable_dict)
        for key, value in variable_dict.items():
            if value == INDEX_PLACE_HOLDER:
                # use eval?
                variable_dict[key] = index
        return variable_dict

    @staticmethod
    def replace_items_with_index(index: int, access_items: list):
        access_items = copy(access_items)
        for i in range(len(access_items)):
            if access_items[i] == INDEX_PLACE_HOLDER:
                access_items[i] = index
        return access_items

    def loop_records(self, loop_num: int, *records: Tuple):
        for index in range(loop_num):
            for record in records:
                self.record(record[0],
                            ChangeList.replace_values_with_index(index, record[1]) if len(record) > 1 else None,
                            ChangeList.replace_items_with_index(index, record[2]) if len(record) > 2 else None
                            )
        return self

    def __eq__(self, other):
        if isinstance(other, list):
            return self.change_list == other
        return False
