from typing import Tuple, Any, List, Set


class Recorder:
    """
    The recoder is used to record variable changes in each step
    the format is a list containing dictionaries::

        [
            {
                'line': 20,
                'variables': {
                    'var1': 'value', 'var2': value, ...
                },
                'accesses': [obj2, obj3, obj1]
            },
            {
                'line': 18,
                'variables': {
                    'var2': 'value', 'var3': 'value', ...
                },
                'accesses': [obj1, obj2]
            },
            ...
        ]
    """
    def __init__(self):
        self.changes: List[dict] = []
        self.variables: Set[Tuple[str, str]] = set()

    def register_variable(self, identifier: Tuple[str, str]) -> None:
        """Register a variable

        a variable is identified by a identifier, which is
        a tuple of two strings. The first strings is the
        name of the place, ie functions etc., in which the
        variable is created. The second string is the variable
        name.
        @param identifier:
        @return:
        """
        self.variables.add(identifier)

    # TODO test this
    def add_record(self, line_no: int = -1) -> None:
        """
        add a record to the change list
        name clarification:
                            - @keyword variables: means variable changes
                            - @keyword accesses: means access changes
        @param line_no: the line number
        """
        self.changes.append({'line': line_no, 'variables': None, 'accesses': None})

    def get_last_record(self) -> dict:
        """
        get the last record
        @return: the last record
        """
        return self.changes[-1]

    def get_previous_record(self) -> dict:
        """Get the second last record in the record list

        In general cases, the first input line may not be
        empty, so `self.changes[-2]` will result in
        IndexError. In this case, we use `self.changes[-1]`
        """
        # this should not be a problem in official use, since the first line in the main function
        # ie. `def main()`: has no variables.
        return self.changes[-2] if len(self.changes) > 1 else self.changes[-1]

    def get_last_vc(self) -> dict:
        """
        get the last variable change dict
        @return: variables dict in the last record
        """
        if not self.get_last_record()['variables']:
            self.get_last_record()['variables'] = {}

        return self.get_last_record()['variables']

    def get_previous_vc(self) -> dict:
        """Get the second last dict in the record list"""
        if not self.get_previous_record()['variables']:
            self.get_previous_record()['variables'] = {}

        return self.get_previous_record()['variables']

    def get_last_ac(self) -> List:
        """
        get the access list from the last record 
        @return: accesses list in the last record
        """
        if not self.get_last_record()['accesses']:
            self.get_last_record()['accesses'] = []
        return self.get_last_record()['accesses']

    def add_vc_to_last_record(self, variable_identifier: Tuple[str, str], variable_state: Any) -> None:
        """
        add a variable change to the last record
        @param variable_identifier: (name_space, variable_name)
        @param variable_state: the variable state
        @return: None
        """
        # if isinstance(variable_change, Tuple):
        self.get_last_vc()[variable_identifier] = variable_state

    def add_vc_to_previous_record(self, variable_identifier: Tuple[str, str], variable_state: Any) -> None:
        """Add variable change to previous (second last if possible) record.

        When the variable is created/changed in line a,
        the tracer evaluate it in line a+1. So, this function
        is created to deal with this offset
        @param variable_identifier:
        @param variable_state:
        @return:
        """
        # if isinstance(variable_change, Tuple) and len(self.changes) > 1:
        self.get_previous_vc()[variable_identifier] = variable_state

    def add_ac_to_last_record(self, access_changes: Any) -> None:
        """
        add an access change to the last record
        @param access_changes: what's accessed
        @return: None
        """
        self.get_last_ac().append(access_changes)

    def purge(self):
        """Empty previous recorded items"""
        self.changes: List[dict] = []
        self.variables: Set[Tuple[str, str]] = set()
