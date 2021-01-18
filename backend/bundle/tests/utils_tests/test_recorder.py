import json
from collections import deque
from numbers import Number
from pprint import pprint
from typing import List, Tuple, Deque, Sequence, Any
from collections import Counter
from collections.abc import Mapping, Set

import pytest

from bundle.seeker import tracer
from bundle.GraphObjects.Edge import Edge
from bundle.GraphObjects.Node import Node
from bundle.utils.recorder import Recorder, identifier_to_string, IDENTIFIER_SEPARATOR
from .recorder_test_util import RecorderResultParser


@pytest.fixture()
def empty_recorder():
    return Recorder()


@pytest.fixture()
def default_identifier_and_string():
    identifier = ('namespace', 'variable')
    return identifier, identifier_to_string(identifier)


@pytest.fixture()
def set_new_recorder():
    tracer.set_new_recorder(Recorder())


def test_identifier_to_string(default_identifier_and_string):
    assert IDENTIFIER_SEPARATOR == u'\u200b@'
    assert default_identifier_and_string[1] == u'namespace\u200b@variable'


def test_assign_color(empty_recorder, default_identifier_and_string):
    default_identifier_string = default_identifier_and_string[1]
    empty_recorder.assign_color(
        default_identifier_string
    )
    assert default_identifier_string in empty_recorder._color_mapping
    assert empty_recorder._color_mapping[default_identifier_string] == empty_recorder._COLOR_PALETTE[2]

    for i in range(20):
        identifier_string = identifier_to_string(
            ('namespace', f'variable{i}')
        )
        empty_recorder.assign_color(identifier_string)

        # two for reserved identifiers
        # one is added manually at the beginning
        # one is just added in the loop
        assert len(empty_recorder._color_mapping) == i + 4


def test_register_variable(empty_recorder):
    identifier = ('namespace', 'variable1')
    identifier_string = identifier_to_string(identifier)
    result_identifier_string = empty_recorder.register_variable(
        identifier
    )

    assert result_identifier_string == identifier_string
    assert identifier_string in empty_recorder._color_mapping


def test_process_variable_state(empty_recorder):
    var_id_string = empty_recorder.register_variable(
        ('namespace', 'var')
    )

    class A:
        pass

    test_mapping = [
        # simple individuals
        1, Number,
        1.2, Number,
        'abc', str,
        Node('id'), Node,
        Edge('ide', (Node('id1'), Node('id2'))), Edge,
        # simple containers
        [1, 2], List,
        (3, 4), Tuple,
        deque([5, 6]), Deque,
        Counter([1, 2, 2, 3, 4, 5, 5, 5]), Counter,
        None, type(None),
        {6, 7, 8}, Set,  # which includes Set, set, KeyView(dict_keys), ItemView(dict_items),
        # frozenset, MutableSet
        {6: 7, 8: 9}.items(), Set,
        {6: 7, 8: 9}.keys(), Set,
        {10: 11, 12: 13}, Mapping,  # which includes mappingproxy (not sure what that is), MutableMapping, dict
        range(1, 10), Sequence,  # which includes tuple, str, range, memoryview, MutableSequence, list, bytearray
        # wildcard
        A(), object
    ]

    for i in range(0, len(test_mapping), 2):
        state_info_mapping = empty_recorder.process_variable_state(
            var_id_string, test_mapping[i]
        )

        assert state_info_mapping[empty_recorder._TYPE_HEADER] == empty_recorder._TYPE_MAPPING[test_mapping[i + 1]]


def test_generating_changes(empty_recorder):
    first_line_no = 1
    empty_recorder.add_record(first_line_no)

    change_list = empty_recorder.get_change_list()

    assert len(change_list) == 1

    first_change = change_list[0]

    assert first_change[empty_recorder._LINE_HEADER] == first_line_no
    assert first_change[empty_recorder._VARIABLE_HEADER] is None
    assert first_change[empty_recorder._ACCESS_HEADER] is None

    first_var_id = ('main', 'var_1')
    first_var_id_string = empty_recorder.register_variable(first_var_id)
    first_var_value = 1
    empty_recorder.add_vc_to_last_record(
        first_var_id_string, first_var_value
    )
    target_type = empty_recorder._TYPE_MAPPING[Number]

    assert first_change[empty_recorder._VARIABLE_HEADER] is not None
    assert first_change[empty_recorder._VARIABLE_HEADER][first_var_id_string][
               empty_recorder._REPR_HEADER] == empty_recorder.custom_repr(first_var_value, target_type, set())
    assert first_change[empty_recorder._VARIABLE_HEADER][first_var_id_string][
               empty_recorder._TYPE_HEADER] == target_type

    accessed_var_value = Node('1')
    empty_recorder.add_ac_to_last_record(
        accessed_var_value
    )
    target_type = empty_recorder._TYPE_MAPPING[Node]
    assert first_change[empty_recorder._ACCESS_HEADER] is not None
    assert first_change[empty_recorder._ACCESS_HEADER][0][empty_recorder._REPR_HEADER] == empty_recorder.custom_repr(
        accessed_var_value, target_type, set())
    assert first_change[empty_recorder._ACCESS_HEADER][0][empty_recorder._TYPE_HEADER] == target_type

    default_start = empty_recorder.get_processed_change_list()[0]
    assert default_start[empty_recorder._LINE_HEADER] == 0
    assert all(item[empty_recorder._TYPE_HEADER] == empty_recorder._INIT_TYPE_STRING and
               item[empty_recorder._REPR_HEADER] is None and
               item[empty_recorder._COLOR_HEADER] is not None
               for item in default_start[empty_recorder._VARIABLE_HEADER].values())


class _Any:
    def __init__(self, v: Any = object):
        self.value = v

    def __eq__(self, other):
        if self.value == object:
            return True
        elif isinstance(other, _Any):
            return self.value == other.value
        else:
            return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)


_anything = _Any()


def test_json_dump(empty_recorder):
    result_string = [{'accesses': None,
                      'line': _anything,
                      'variables': {'main\u200b@var_1': {'color': '#A6CEE3',
                                                         'repr': None,
                                                         'type': 'init'},
                                    'main\u200b@var_2': {'color': '#1F78B4',
                                                         'repr': None,
                                                         'type': 'init'},
                                    'main\u200b@var_3': {'color': '#B2DF8A',
                                                         'repr': None,
                                                         'type': 'init'},
                                    'main\u200b@var_4': {'color': '#33A02C',
                                                         'repr': None,
                                                         'type': 'init'}}},
                     {'accesses': [{'color': '#B15928',
                                    'id': _anything,
                                    'properties': {'color': '#828282',
                                                   'python_id': _anything,
                                                   'repr': [],
                                                   'type': 'Mapping'},
                                    'python_id': _anything,
                                    'repr': 'Node(1)',
                                    'type': 'Node'}],
                      'line': _anything,
                      'variables': {'main\u200b@var_1': {'color': '#A6CEE3',
                                                         'python_id': _anything,
                                                         'repr': '1',
                                                         'type': 'Number'},
                                    'main\u200b@var_2': {'color': '#1F78B4',
                                                         'id': _anything,
                                                         'properties': {'color': '#828282',
                                                                        'python_id': _anything,
                                                                        'repr': [],
                                                                        'type': 'Mapping'},
                                                         'python_id': _anything,
                                                         'repr': 'Node(1)',
                                                         'type': 'Node'},
                                    'main\u200b@var_3': {'color': '#B2DF8A',
                                                         'repr': None,
                                                         'type': 'init'},
                                    'main\u200b@var_4': {'color': '#33A02C',
                                                         'python_id': _anything,
                                                         'repr': 'None',
                                                         'type': 'None'}}},
                     {'accesses': [{'color': '#B15928',
                                    'python_id': _anything,
                                    'repr': [{'key': {'color': '#828282',
                                                      'python_id': _anything,
                                                      'repr': '1',
                                                      'type': 'Number'},
                                              'value': {'color': '#828282',
                                                        'python_id': _anything,
                                                        'repr': [{'key': {'color': '#828282',
                                                                          'python_id': _anything,
                                                                          'repr': '2',
                                                                          'type': 'Number'},
                                                                  'value': {'color': '#828282',
                                                                            'python_id': _anything,
                                                                            'repr': '3',
                                                                            'type': 'Number'}},
                                                                 {'key': {'color': '#828282',
                                                                          'python_id': _anything,
                                                                          'repr': '4',
                                                                          'type': 'Number'},
                                                                  'value': {'color': '#828282',
                                                                            'python_id': _anything,
                                                                            'repr': '5',
                                                                            'type': 'Number'}}],
                                                        'type': 'Mapping'}},
                                             {'key': {'color': '#828282',
                                                      'python_id': _anything,
                                                      'repr': [{'color': '#828282',
                                                                'python_id': _anything,
                                                                'repr': '6',
                                                                'type': 'Number'},
                                                               {'color': '#828282',
                                                                'python_id': _anything,
                                                                'repr': '7',
                                                                'type': 'Number'},
                                                               {'color': '#828282',
                                                                'python_id': _anything,
                                                                'repr': '8',
                                                                'type': 'Number'}],
                                                      'type': 'Tuple'},
                                              'value': {'color': '#828282',
                                                        'python_id': _anything,
                                                        'repr': '9',
                                                        'type': 'Number'}}],
                                    'type': 'Mapping'}],
                      'line': _anything,
                      'variables': {'main\u200b@var_1': {'color': '#A6CEE3',
                                                         'python_id': _anything,
                                                         'repr': '1',
                                                         'type': 'Number'},
                                    'main\u200b@var_2': {'color': '#1F78B4',
                                                         'id': _anything,
                                                         'properties': {'color': '#828282',
                                                                        'python_id': _anything,
                                                                        'repr': [],
                                                                        'type': 'Mapping'},
                                                         'python_id': _anything,
                                                         'repr': 'Node(1)',
                                                         'type': 'Node'},
                                    'main\u200b@var_3': {'color': '#B2DF8A',
                                                         'python_id': _anything,
                                                         'repr': "'ab'",
                                                         'type': 'String'},
                                    'main\u200b@var_4': {'color': '#33A02C',
                                                         'python_id': _anything,
                                                         'repr': 'None',
                                                         'type': 'None'}}},
                     {'accesses': None, 'line': _anything, 'variables': None}]
    first_line_no = 1
    empty_recorder.add_record(first_line_no)

    first_var_id = ('main', 'var_1')
    first_var_id_string = empty_recorder.register_variable(first_var_id)
    first_var_value = 1
    empty_recorder.add_vc_to_last_record(
        first_var_id_string, first_var_value
    )

    second_var_id = ('main', 'var_2')
    second_var_id_string = empty_recorder.register_variable(second_var_id)
    second_var_value = Node('1')
    empty_recorder.add_vc_to_last_record(
        second_var_id_string, second_var_value
    )

    first_accessed_var_value = Node('1')
    empty_recorder.add_ac_to_last_record(
        first_accessed_var_value
    )

    second_line_no = 2
    empty_recorder.add_record(second_line_no)

    third_var_id = ('main', 'var_3')
    third_var_id_string = empty_recorder.register_variable(third_var_id)
    third_var_value = 'abc'
    empty_recorder.add_vc_to_last_record(
        third_var_id_string, third_var_value
    )

    fourth_var_id = ('main', 'var_4')
    fourth_var_id_string = empty_recorder.register_variable(fourth_var_id)
    fourth_var_value = None
    empty_recorder.add_vc_to_previous_record(
        fourth_var_id_string, fourth_var_value
    )

    second_accessed_var_value = {
        1: {
            2: 3,
            4: 5
        },
        (6, 7, 8): 9
    }
    empty_recorder.add_ac_to_last_record(
        second_accessed_var_value
    )

    third_line_no = 20
    empty_recorder.add_record(third_line_no)

    third_var_value = 'ab'
    empty_recorder.add_vc_to_previous_record(
        third_var_id_string, third_var_value
    )

    assert json.loads(empty_recorder.get_change_list_json()) == result_string
    # print(empty_recorder.get_change_list_json())


def test_recursive(set_new_recorder):
    result = [{'accesses': None,
               'line': _anything,
               'variables': {'t\u200b@a': {'color': '#A6CEE3',
                                           'repr': None,
                                           'type': 'init'}}},
              {'accesses': None, 'line': _anything, 'variables': None},
              {'accesses': None,
               'line': _anything,
               'variables': {'t\u200b@a': {'color': '#A6CEE3',
                                           'python_id': _anything,
                                           'repr': [],
                                           'type': 'List'}}},
              {'accesses': None, 'line': _anything, 'variables': None},
              {'accesses': None,
               'line': _anything,
               'variables': {'t\u200b@a': {'color': '#A6CEE3',
                                           'python_id': _anything,
                                           'repr': [{'color': '#828282',
                                                     'python_id': _anything,
                                                     'repr': [{'color': '#828282',
                                                               'python_id': _anything,
                                                               'repr': '1',
                                                               'type': 'Number'},
                                                              {'color': '#828282',
                                                               'python_id': _anything,
                                                               'repr': '2',
                                                               'type': 'Number'},
                                                              {'color': '#828282',
                                                               'python_id': _anything,
                                                               'repr': '3',
                                                               'type': 'Number'},
                                                              {'color': '#828282',
                                                               'python_id': _anything,
                                                               'repr': None,
                                                               'type': 'reference'}],
                                                     'type': 'List'}],
                                           'type': 'List'}}},
              {'accesses': None,
               'line': _anything,
               'variables': {'t\u200b@a': {'color': '#A6CEE3',
                                           'python_id': _anything,
                                           'repr': [{'color': '#828282',
                                                     'python_id': _anything,
                                                     'repr': [{'color': '#828282',
                                                               'python_id': _anything,
                                                               'repr': '1',
                                                               'type': 'Number'},
                                                              {'color': '#828282',
                                                               'python_id': _anything,
                                                               'repr': '2',
                                                               'type': 'Number'},
                                                              {'color': '#828282',
                                                               'python_id': _anything,
                                                               'repr': '3',
                                                               'type': 'Number'},
                                                              {'color': '#828282',
                                                               'python_id': _anything,
                                                               'repr': None,
                                                               'type': 'reference'}],
                                                     'type': 'List'},
                                                    {'color': '#828282',
                                                     'python_id': _anything,
                                                     'repr': '4',
                                                     'type': 'Number'}],
                                           'type': 'List'}}}]

    @tracer('a')
    def t():
        a = []
        b = [1, 2, 3, a]
        a.append(b)
        a.append(4)

    t()
    assert RecorderResultParser(tracer.get_recorder().get_processed_change_list()) == RecorderResultParser(result)


def test_one_func_assign(set_new_recorder):
    @tracer('a')
    def main():
        a = 10

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 442, 'variables': None},
              {'accesses': None,
               'line': 443,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4334516816,
                                              'repr': '10',
                                              'type': 'Number'}}}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())


def test_end_of_func_modify(set_new_recorder):
    @tracer('a')
    def main():
        a = ''
        a = 1

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 456, 'variables': None},
              {'accesses': None,
               'line': 457,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4374603376,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None,
               'line': 458,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4374415664,
                                              'repr': '1',
                                              'type': 'Number'}}}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())


def test_end_of_func_new_var(set_new_recorder):
    @tracer('a', 'b')
    def main():
        a = ''
        b = 1

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'},
                             'main\u200b@b': {'color': '#1F78B4',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 484, 'variables': None},
              {'accesses': None,
               'line': 485,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4514518640,
                                              'repr': "''",
                                              'type': 'String'},
                             'main\u200b@b': {'color': '#1F78B4',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None,
               'line': 486,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4514518640,
                                              'repr': "''",
                                              'type': 'String'},
                             'main\u200b@b': {'color': '#1F78B4',
                                              'python_id': 4514330928,
                                              'repr': '1',
                                              'type': 'Number'}}}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())


def test_call_not_traced_func_return_val(set_new_recorder):
    def call_test(a: int = 2):
        a **= a
        return a

    @tracer('a', 'b')
    def main():
        a = ''
        a = call_test()

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 529, 'variables': None},
              {'accesses': None,
               'line': 530,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4341716592,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None,
               'line': 531,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4341528880,
                                              'repr': '4',
                                              'type': 'Number'}}}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())


def test_call_not_traced_func_return_none(set_new_recorder):
    def call_test(a: int = 2):
        a **= a

    @tracer('a', 'b')
    def main():
        a = ''
        call_test()

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 563, 'variables': None},
              {'accesses': None,
               'line': 564,
               'variables': {'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4509455984,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None, 'line': 565, 'variables': None}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())


def test_call_traced_func_default_val_no_return(set_new_recorder):
    @tracer('a')
    def call_test(a: int = 2):
        a **= a

    @tracer('a', 'b')
    def main():
        a = ''
        call_test()

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 593, 'variables': None},
              {'accesses': None,
               'line': 594,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4449818224,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None, 'line': 595, 'variables': None},
              {'accesses': None,
               'line': 589,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'python_id': 4449630544,
                                                   'repr': '2',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4449818224,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None,
               'line': 590,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'python_id': 4449630608,
                                                   'repr': '4',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4449818224,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None, 'line': 595, 'variables': None}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())


def test_call_traced_func_default_var_return_val(set_new_recorder):
    @tracer('a')
    def call_test(a: int = 2):
        a **= a
        return a

    @tracer('a', 'b')
    def main():
        a = ''
        a = call_test()

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 651, 'variables': None},
              {'accesses': None,
               'line': 652,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4435457648,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None, 'line': 653, 'variables': None},
              {'accesses': None,
               'line': 646,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'python_id': 4435269968,
                                                   'repr': '2',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4435457648,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None,
               'line': 647,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'python_id': 4435270032,
                                                   'repr': '4',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4435457648,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None, 'line': 648, 'variables': None},
              {'accesses': None,
               'line': 653,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'python_id': 4435270032,
                                                   'repr': '4',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4435270032,
                                              'repr': '4',
                                              'type': 'Number'}}}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())


def test_call_traced_func_no_default_val(set_new_recorder):
    @tracer('a')
    def call_test(a):
        a **= a
        return a

    @tracer('a', 'b')
    def main():
        a = ''
        a = call_test(3)

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 719, 'variables': None},
              {'accesses': None,
               'line': 720,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4500768368,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None, 'line': 721, 'variables': None},
              {'accesses': None,
               'line': 714,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'python_id': 4500580720,
                                                   'repr': '3',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4500768368,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None,
               'line': 715,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'python_id': 4500581488,
                                                   'repr': '27',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4500768368,
                                              'repr': "''",
                                              'type': 'String'}}},
              {'accesses': None, 'line': 716, 'variables': None},
              {'accesses': None,
               'line': 721,
               'variables': {'call_test\u200b@a': {'color': '#1F78B4',
                                                   'python_id': 4500581488,
                                                   'repr': '27',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4500581488,
                                              'repr': '27',
                                              'type': 'Number'}}}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())


def test_call_traced_func_new_var(set_new_recorder):
    @tracer('b')
    def call_test(c):
        b = c ** c
        return b

    @tracer('a', 'b')
    def main():
        a = ''
        b = call_test(3)

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'call_test\u200b@b': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'},
                             'main\u200b@b': {'color': '#B2DF8A',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 787, 'variables': None},
              {'accesses': None,
               'line': 788,
               'variables': {'call_test\u200b@b': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4430603888,
                                              'repr': "''",
                                              'type': 'String'},
                             'main\u200b@b': {'color': '#B2DF8A',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 789, 'variables': None},
              {'accesses': None, 'line': 782, 'variables': None},
              {'accesses': None,
               'line': 783,
               'variables': {'call_test\u200b@b': {'color': '#1F78B4',
                                                   'python_id': 4430417008,
                                                   'repr': '27',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4430603888,
                                              'repr': "''",
                                              'type': 'String'},
                             'main\u200b@b': {'color': '#B2DF8A',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 784, 'variables': None},
              {'accesses': None,
               'line': 789,
               'variables': {'call_test\u200b@b': {'color': '#1F78B4',
                                                   'python_id': 4430417008,
                                                   'repr': '27',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4430603888,
                                              'repr': "''",
                                              'type': 'String'},
                             'main\u200b@b': {'color': '#B2DF8A',
                                              'python_id': 4430417008,
                                              'repr': '27',
                                              'type': 'Number'}}}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())


def test_call_traced_func_direct_return(set_new_recorder):
    @tracer('c')
    def call_test(c):
        return c ** c

    @tracer('a', 'b')
    def main():
        a = ''
        b = call_test(3)

    main()

    result = [{'accesses': None,
               'line': 0,
               'variables': {'call_test\u200b@c': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'repr': None,
                                              'type': 'init'},
                             'main\u200b@b': {'color': '#B2DF8A',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 858, 'variables': None},
              {'accesses': None,
               'line': 859,
               'variables': {'call_test\u200b@c': {'color': '#1F78B4',
                                                   'repr': None,
                                                   'type': 'init'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4490438256,
                                              'repr': "''",
                                              'type': 'String'},
                             'main\u200b@b': {'color': '#B2DF8A',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 860, 'variables': None},
              {'accesses': None,
               'line': 854,
               'variables': {'call_test\u200b@c': {'color': '#1F78B4',
                                                   'python_id': 4490250608,
                                                   'repr': '3',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4490438256,
                                              'repr': "''",
                                              'type': 'String'},
                             'main\u200b@b': {'color': '#B2DF8A',
                                              'repr': None,
                                              'type': 'init'}}},
              {'accesses': None, 'line': 855, 'variables': None},
              {'accesses': None,
               'line': 860,
               'variables': {'call_test\u200b@c': {'color': '#1F78B4',
                                                   'python_id': 4490250608,
                                                   'repr': '3',
                                                   'type': 'Number'},
                             'main\u200b@a': {'color': '#A6CEE3',
                                              'python_id': 4490438256,
                                              'repr': "''",
                                              'type': 'String'},
                             'main\u200b@b': {'color': '#B2DF8A',
                                              'python_id': 4490251376,
                                              'repr': '27',
                                              'type': 'Number'}}}]

    assert RecorderResultParser(result) == RecorderResultParser(tracer.get_recorder().get_processed_change_list())
    pprint(tracer.get_recorder().get_processed_change_list())
