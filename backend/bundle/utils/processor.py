from typing import Tuple, Mapping


def make_tuple(var) -> Tuple:
    return var,


class Processor:
    """
    Processor should return the state at that line if changes took place in the code
    if some variables are not changed, I will record it's value. If it's empty, the corresponding
    value will be set to none.
    """
    def __init__(self, variable_number_limit: int = 10):
        # TODO put the register work to recorder
        self.variable_number_limit = variable_number_limit
        self.variable_color_map: Mapping = None
        self.result_json: Mapping = None

    def create_color_map(self) -> None:
        pass

    def get_result_json(self) -> Mapping:
        if not self.result_json:
            self.generate_result_json()
        return self.result_json

    def generate_result_json(self) -> None:
        pass
