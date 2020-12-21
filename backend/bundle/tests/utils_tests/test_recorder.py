import pytest
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
