from uuid import UUID

import pytest

from backend.intel_wrappers.intel_wrapper import UploadsWrapper
from backend.intel_wrappers.validators import ValidationError
from backend.model.TutorialRelatedModel import FAKE_UUID
from tests.wrapper_test.test_wrapper_helper import gen_wrapper_test_class, FIXTURE_HEADER


# for pycharm quick start
class TestUploadsWrapper:
    def test_func(self):
        pass


ADDON_FILE = FIXTURE_HEADER + 'add_on_test_file'

# noinspection PyRedeclaration
TestUploadsWrapper = gen_wrapper_test_class(wrapper_class=UploadsWrapper, test_params={
    'test_load': [
        pytest.param('stored_uploads', True),
        pytest.param('stored_uploads', False)
    ],
    'test_set_variables': [
        pytest.param({

        }, id='empty_variables'),
        pytest.param({
            'file': FIXTURE_HEADER + 'add_on_test_file'
        }),
        pytest.param({
            'file': FIXTURE_HEADER + 'add_on_test_file',
            'alias': 'test set var'
        })
    ],
    'test_making_new_model': [
        {
            'file': ADDON_FILE,
            'alias': 'test set var'
        }
    ],
    'test_retrieve_model': [
        pytest.param('stored_uploads', {'id': UUID('d4c31662-2de5-44c3-af1d-bad04360dab1'), }, id='fetch by id'),
        pytest.param('stored_uploads', {'alias': 'uploads store testing', }, id='fetch by alias'),
        # pytest.param('stored_uploads', {'file': str(pathlib.Path(_STORED_TEST_FILE)), }, id='fetch by file string'),
        # pytest.param('stored_uploads', {'file': File(open(_STORED_TEST_FILE)), }, id='fetch by file object'),
    ],
    'test_overwrite': [
        pytest.param(None, {}, marks=pytest.mark.skip('not applicable')),
    ],
    'test_validation': [
        pytest.param({'file': None}, ValidationError, None,
                     id='invalid file'),
        pytest.param({'file': ADDON_FILE, 'alias': object()}, ValidationError, None,
                     id='invalid code')
    ],
    'test_get_model': [
        pytest.param(None, {
            'file': FIXTURE_HEADER + 'add_on_test_file',
            'alias': 'test set var'
        }, False, False, AssertionError, 'Cannot make new model without validations!',
                     id='no_validate_no_model_assertion_err'),
        pytest.param(None, {
            'file': FIXTURE_HEADER + 'add_on_test_file',
            'alias': 'test set var'
        }, True, True, None, None, id='make_new_model'),
        pytest.param('one_time_uploads', {
            'id': UUID('b6150a4e-f8bb-4f46-932d-9cb80b1279b5'),
            'file': FIXTURE_HEADER + 'add_on_test_file',
            'alias': 'test set var'
        }, True, False, None, None, id='overwrite_model', marks=pytest.mark.skip(reason='not applicable')),
    ],
    'test_finalize': [
        pytest.param(None, {
            'file': FIXTURE_HEADER + 'add_on_test_file',
            'alias': object()
        }, True, True, ValidationError, None),
        pytest.param(None, {
            'file': FIXTURE_HEADER + 'add_on_test_file',
            'alias': 'test finalize',
        }, True, True, None, None),
        pytest.param(None, {
            'file': FIXTURE_HEADER + 'add_on_test_file',
            'alias': 'test finalize'
        }, False, True, AssertionError, None),
        pytest.param(None, {
            'file': FIXTURE_HEADER + 'add_on_test_file',
            'alias': 'test finalize'
        }, True, False, AssertionError, None),
    ]
}, default_params={'is_published': False, 'id': FAKE_UUID})
