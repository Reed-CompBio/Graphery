import pytest
from bundle.controller import controller


@pytest.fixture()
def use_samples():
    with controller as folder_crater, folder_crater():
        from tests.seeker_tests.samples import recorder as samples
        yield samples


@pytest.mark.skip
def test_simple_loop(use_samples):
    use_samples.simple_loop_trace_non()
    assert ChangeList() \
               .record(5) \
               .loop_records(10, (6,), (7,)) \
               .record(6) \
               .change_list == controller.get_recorded_content()


@pytest.mark.skip
def test_simple_loop_trace_index(use_samples):
    use_samples.simple_loop_trace_index()
    print(use_samples.tracer.get_recorder_change_list())
    # TODO write a useful test.
    assert ChangeList() \
           .record(11) \
           .loop_records(10, (12, {'i': INDEX_PLACE_HOLDER}), (13,)) \
           .record(12) \
           .change_list  # == controller.get_recorded_content()


@pytest.mark.skip
def test_simple_while_loop_trace_index(use_samples):
    use_samples.simple_while_loop_trace_index()
    assert ChangeList() \
           .record(17) \
           .record(18, {'i': 0})
    # TODO sigh
