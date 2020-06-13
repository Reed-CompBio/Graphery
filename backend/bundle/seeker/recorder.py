from typing import Tuple, Any, List


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

    def get_last_vc(self) -> dict:
        """
        get the last variable change dict
        @return: variables dict in the last record
        """
        if not self.get_last_record()['variables']:
            self.get_last_record()['variables'] = {}

        return self.get_last_record()['variables']

    def get_last_ac(self) -> List:
        """
        get the access list from the last record 
        @return: accesses list in the last record
        """
        if not self.get_last_record()['accesses']:
            self.get_last_record()['accesses'] = []
        return self.get_last_record()['accesses']

    def add_vc_to_last_record(self, variable_change: Tuple[str, Any]) -> None:
        """
        add a variable change to the last record
        @param variable_change: (accessed variable name, variable content)
        @return: None
        """
        if isinstance(variable_change, Tuple):
            self.get_last_vc()[variable_change[0]] = variable_change[1] 

    def add_ac_to_last_record(self, access_changes: Any) -> None:
        """
        add an access change to the last record
        @param access_changes: what's accessed
        @return: None
        """
        self.get_last_ac().append(access_changes)


class GraphRecorder(Recorder):
    """
    A recorder dedicated to graph objects
    @note: I don't think I need it
    """
    def __init__(self):
        super(Recorder, self).__init__()
