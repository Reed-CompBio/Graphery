from collections import deque
from numbers import Number
from typing import List, Tuple, Deque, Sequence
from collections import Counter
from collections.abc import Mapping, Set

import pytest

from bundle.GraphObjects.Edge import Edge
from bundle.GraphObjects.Node import Node
from bundle.controller import controller
from bundle.utils.recorder import Recorder, identifier_to_string, IDENTIFIER_SEPARATOR


@pytest.fixture()
def use_samples():
    with controller as folder_crater, folder_crater():
        from tests.seeker_tests.samples import recorder as samples
        yield samples


@pytest.fixture()
def empty_recorder():
    return Recorder()


@pytest.fixture()
def default_identifier_and_string():
    identifier = ('namespace', 'variable')
    return identifier, identifier_to_string(identifier)


def test_identifier_to_string(default_identifier_and_string):
    assert IDENTIFIER_SEPARATOR == u'\u200b@'
    assert default_identifier_and_string[1] == u'namespace\u200b@variable'


def test_assign_color(empty_recorder, default_identifier_and_string):
    default_identifier_string = default_identifier_and_string[1]
    empty_recorder.assign_color(
        default_identifier_string
    )
    assert default_identifier_string in empty_recorder._color_mapping
    assert empty_recorder._color_mapping[default_identifier_string] == empty_recorder._COLOR_PALETTE[0]

    for i in range(20):
        identifier_string = identifier_to_string(
            ('namespace', f'variable{i}')
        )
        empty_recorder.assign_color(identifier_string)
        assert len(empty_recorder._color_mapping) == i + 2


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
    change_list = empty_recorder.get_change_list()
    first_line_no = 1
    empty_recorder.add_record(first_line_no)
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
    assert first_change[empty_recorder._VARIABLE_HEADER][first_var_id_string][empty_recorder._REPR_HEADER] == empty_recorder.custom_repr(first_var_value, target_type)
    assert first_change[empty_recorder._VARIABLE_HEADER][first_var_id_string][empty_recorder._TYPE_HEADER] == target_type

    accessed_var_value = Node('1')
    empty_recorder.add_ac_to_last_record(
        accessed_var_value
    )
    target_type = empty_recorder._TYPE_MAPPING[Node]
    assert first_change[empty_recorder._ACCESS_HEADER] is not None
    assert first_change[empty_recorder._ACCESS_HEADER][0][empty_recorder._REPR_HEADER] == empty_recorder.custom_repr(accessed_var_value, target_type)
    assert first_change[empty_recorder._ACCESS_HEADER][0][empty_recorder._TYPE_HEADER] == target_type


def test_json_dump(empty_recorder):
    pass
