from uuid import UUID

import pytest

from backend.intel_wrappers.intel_wrapper import CategoryWrapper
from backend.intel_wrappers.validators import ValidationError
from tests.wrapper_test.test_wrapper_helper import gen_wrapper_test_class


# for pycharm quick start
class TestCategoryWrapper:
    def test_func(self):
        pass


# noinspection PyRedeclaration
TestCategoryWrapper = gen_wrapper_test_class(wrapper_class=CategoryWrapper, test_params={
    'test_load': [
        pytest.param('stored_mock_category', True),
        pytest.param('stored_mock_category', False)
    ],
    'test_set_variables': [
        pytest.param({

        }, id='empty_variables'),
        pytest.param({
            'category': 'set_var_category'
        }),
        pytest.param({
            'category': 'set_var_category',
            'is_published': False
        })
    ],
    'test_making_new_model': [
        {
            'category': 'set_var_category',
            'is_published': False
        }
    ],
    'test_retrieve_model': [
        pytest.param('stored_mock_category', {'id': UUID('a58912ae-0343-4827-9dc1-b8518faf13ff'), }, ),
    ],
    'test_overwrite': [
        pytest.param('temp_mock_category', {'category': 'mock_category_mod'}, ),
        pytest.param('temp_mock_category', {'category': 'mock_category_mod', 'is_published': False}),
    ],
    'test_validation': [
        pytest.param({'category': 'err-'}, ValidationError,
                     r'`category` must be a non-empty string and does not start or end with `-` or `_`.',
                     id='category_string_error'),
        pytest.param({'category': 'type', 'is_published': 'a'}, ValidationError,
                     r'`is_published` must be a boolean variable!',
                     id='is_published_error')
    ],
    'test_get_model': [
        pytest.param(None, {
            'category': 'get_model_cat'
        }, True, False, AssertionError, 'Cannot make new model without validations!',
                     id='no_validate_no_model_assertion_err'),
        pytest.param('stored_mock_category', {
            'category': 'get_model_cat',
            'is_published': False
        }, True, False, AssertionError, 'Cannot overwrite model without validations!',
                     id='no_validate_cant_overwrite_err'),
        pytest.param(None, {
            'category': 'get_model_cat',
            'is_published': False
        }, True, True, None, None, id='make_new_model'),
        pytest.param('stored_mock_category', {
            'category': 'get_model_cat_mod'
        }, True, True, None, None, id='overwrite_model'),
    ]
}, default_params={'is_published': False})
