import pytest
from bundle.tests.seeker_tests.recorder_utils import *
from bundle.controller import controller


@pytest.fixture()
def use_samples():
    with controller():
        from bundle.tests.seeker_tests.samples import recorder as samples
        yield samples


def test_simple_loop(use_samples):
    use_samples.simple_loop_trace_non()
    assert ChangeList() \
               .record(5) \
               .loop_records(10, (6,), (7,)) \
               .record(6) \
               .change_list == controller.get_recorded_content()


def test_simple_loop_trace_index(use_samples):
    use_samples.simple_loop_trace_index()
    assert ChangeList() \
           .record(11) \
           .loop_records(10, (12, {'i': INDEX_PLACE_HOLDER}), (13,)) \
           .record(12) \
           .change_list == controller.get_recorded_content()


def test_simple_while_loop_trace_index(use_samples):
    use_samples.simple_while_loop_trace_index()
    assert ChangeList() \
           .record(17) \
           .record(18, {'i': 0})
    # TODO sigh
