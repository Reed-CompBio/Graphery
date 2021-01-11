from uuid import UUID

import pytest

from backend.intel_wrappers.intel_wrapper import CodeWrapper
from backend.intel_wrappers.validators import ValidationError
from tests.wrapper_test.factories import tutorial_anchor_wrapper_factory
from tests.wrapper_test.test_wrapper_helper import gen_wrapper_test_class


# for pycharm quick start
class TestCodeWrapper:
    def test_func(self):
        pass


# noinspection PyRedeclaration
TestCodeWrapper = gen_wrapper_test_class(wrapper_class=CodeWrapper, test_params={
    'test_load': [
        pytest.param('stored_mock_code', True),
        pytest.param('stored_mock_code', False)
    ],
    'test_set_variables': [
        pytest.param({

        }, id='empty_variables'),
        pytest.param({
            'code': 'code'
        }),
        pytest.param({
            'code': 'code',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='code-tutorial-url',
                name_template='code tutorial name'
            )
        }),
        pytest.param({
            'name': 'test set var',
            'code': 'code',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='code-tutorial-url',
                name_template='code tutorial name'
            )
        })
    ],
    'test_making_new_model': [
        {
            'name': 'test make new model',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='make new model',
                name_template='make new model'
            ),
            'code': 'code'
        }
    ],
    'test_retrieve_model': [
        pytest.param('stored_mock_code', {'id': UUID('24d137dc-5cc2-4ace-b71c-e5b9386a2281'), }, ),
    ],
    'test_overwrite': [
        pytest.param('one_time_mock_code', {
            'name': 'test overwrite'
        }),
        pytest.param('one_time_mock_code', {
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='overwrite-tutorial-url',
                name_template='overwrite tutorial'
            )
        }),
        pytest.param('one_time_mock_code', {
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='overwrite-tutorial-url',
                name_template='overwrite tutorial'
            ),
            'code': 'overwrite code'
        }),
    ],
    'test_validation': [
        pytest.param({'name': None}, ValidationError, None),
        pytest.param({'name': 'name', 'tutorial': None}, AttributeError, None,
                     id='invalid tutorial'),
        pytest.param({'name': 'name',
                      'tutorial': tutorial_anchor_wrapper_factory(
                          url_template='test-validation',
                          name_template='test validation'
                      ), 'code': None}, ValidationError, None,
                     id='invalid code')
    ],
    'test_get_model': [
        pytest.param(None, {
            'name': 'test get model',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='test-get-model-url',
                name_template='test get model'
            ),
            'code': 'test get model'
        }, False, False, AssertionError, 'Cannot make new model without validations!',
                     id='no_validate_no_model_assertion_err'),
        pytest.param(None, {
            'name': 'test get new model',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='test-get-model-url',
                name_template='test get model'
            ),
            'code': 'test get model'
        }, True, True, None, None, id='make_new_model'),
        pytest.param('one_time_mock_code', {
            'name': 'test get old model',
            'id': UUID('8ceb0d01-cd29-4fe9-a37b-758b8e6d943c'),
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='test-get-model-url',
                name_template='test get model'
            ),
            'code': 'test get model'
        }, True, False, None, None, id='overwrite_model'),
    ],
    'test_finalize': [
        pytest.param('one_time_mock_code', {
            'name': 'test finalize model',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='test-finalize-model-url',
                name_template='test finalize model'
            ),
            'code': 'test finalize model'
        }, True, True, None, None),
        pytest.param('one_time_mock_code', {
            'name': 'test finalize model no overwrite',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='test-finalize-model-url',
                name_template='test finalize model'
            ),
            'code': 'test finalize model'
        }, True, False, None, None),
        pytest.param('one_time_mock_code', {
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='test-finalize-model-url',
                name_template='test finalize model'
            ),
        }, True, True, None, None),
        pytest.param('one_time_mock_code', {
            'code': 1
        }, True, True, ValidationError, None),
        pytest.param(None, {
            'name': 'test finalize new model',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='test-finalize-model-url',
                name_template='test finalize model'
            ),
            'code': 'test finalize model'
        }, True, True, None, None),
        pytest.param(None, {
            'name': 'test finalize new model',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='test-finalize-model-url',
                name_template='test finalize model'
            ),
            'code': 'test finalize model'
        }, False, True, AssertionError, None),
        pytest.param(None, {
            'name': 'test finalize new model',
            'tutorial': tutorial_anchor_wrapper_factory(
                url_template='test-finalize-model-url',
                name_template='test finalize model'
            ),
            'code': 'test finalize model'
        }, True, False, AssertionError, None),
    ]
}, default_params={'is_published': False})
