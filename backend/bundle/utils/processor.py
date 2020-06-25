from typing import Tuple, Mapping


def make_tuple(var) -> Tuple:
    return var,


class Processor:
    def __init__(self, variable_number_limit: int = 10):
        self.variables = set()
        self.variable_number_limit = variable_number_limit
        self.variable_color_map: Mapping = None
        self.result_json: Mapping = None

    def register_variable(self, variable) -> None:
        if len(self.variables) >= self.variable_number_limit:
            raise AssertionError('You cannot trace more than 10 variables')
        self.variables.add(make_tuple(variable))

    def clear_storage(self) -> None:
        self.variables = set()

    def create_color_map(self) -> None:
        pass

    def get_result_json(self) -> Mapping:
        if not self.result_json:
            self.generate_result_json()
        return self.result_json

    def generate_result_json(self) -> None:
        pass
