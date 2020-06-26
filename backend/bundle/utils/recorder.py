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
        self.variables.add(identifier)

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
        return self.changes[-2]

    def get_last_vc(self) -> dict:
        """
        get the last variable change dict
        @return: variables dict in the last record
        """
        if not self.get_last_record()['variables']:
            self.get_last_record()['variables'] = {}

        return self.get_last_record()['variables']

    def get_previous_vc(self) -> dict:
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
        # if isinstance(variable_change, Tuple) and len(self.changes) > 1:
        self.get_previous_vc()[variable_identifier] = variable_state

    def add_ac_to_last_record(self, access_changes: Any) -> None:
        """
        add an access change to the last record
        @param access_changes: what's accessed
        @return: None
        """
        self.get_last_ac().append(access_changes)
