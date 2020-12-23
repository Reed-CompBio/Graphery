import pytest
from bundle.controller import _Controller


@pytest.fixture()
def new_controller():
    return _Controller()


@pytest.mark.parametrize('auto_delete', [
    True, False
])
def test_controller_creation(auto_delete):
    default_path_auto_delete_controller = _Controller(auto_delete=auto_delete)
    assert default_path_auto_delete_controller.log_folder.exists()
    log_folder = default_path_auto_delete_controller.log_folder
    del default_path_auto_delete_controller
    assert not log_folder.exists() == auto_delete


def test_controller_logging(new_controller):
    assert new_controller.log_folder.exists()
    assert new_controller.tracer_cls._logger is None


def test_controller_enter_and_exit(new_controller):
    with new_controller as folder_generator, folder_generator() as work_folder:
        assert work_folder.exists()
        assert new_controller.tracer_cls._logger is not None
    assert new_controller.tracer_cls._logger is None


def test_controller_working(new_controller):
    with new_controller as folder_generator, folder_generator():
        @new_controller.tracer_cls('a')
        def mock_func():
            a = 'hello world'

        mock_func()
