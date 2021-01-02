import pytest

from backend.intel_wrappers.intel_wrapper import UserWrapper
from backend.intel_wrappers.validators import ValidationError
from backend.model.UserModel import ROLES
from tests.wrapper_test.test_wrapper_helper import gen_wrapper_test_class


# for pycharm quick start
class TestUserWrapper:
    def test_func(self):
        pass


# noinspection PyRedeclaration
TestUserWrapper = gen_wrapper_test_class(wrapper_class=UserWrapper, test_params={
    'test_load': [
        pytest.param('stored_mock_user', True),
        pytest.param('stored_mock_user', False)
    ],
    'test_set_variables': [
        pytest.param({
            'email': 'set_user@email.com',
            'username': 'set_user',
            'first_name': 'set',
            'last_name': 'user',
            'role': ROLES.VISITOR,
        }),
        pytest.param({
            'email': 'set_user@email.com',
            'last_name': 'user',
            'role': ROLES.VISITOR,
        }),
        pytest.param({
            'last_name': 'user',
        }),
        pytest.param({

        })
    ],
    'test_making_new_model': [
        pytest.param({
            'email': 'new_user@email.com',
            'username': 'new_user',
            'first_name': 'new',
            'last_name': 'user',
            'role': ROLES.VISITOR,
        }),
    ],
    'test_retrieve_model': [
        pytest.param('stored_mock_user', {'username': 'mock_user', },
                     marks=pytest.mark.xfail(raises=UserWrapper.model_class.DoesNotExist)),
        pytest.param('stored_mock_user', {'email': 'mock_user@test.com', },
                     marks=pytest.mark.xfail(raises=UserWrapper.model_class.DoesNotExist)),
        pytest.param('stored_mock_user', {'username': 'mock_user', 'email': 'mock_user@test.com', }),
    ],
    'test_overwrite': [
        pytest.param('temp_mock_user', {'username': 'mock_user_modified'}, ),
        pytest.param('temp_mock_user', {
            'username': 'mock_user_modified',
            'email': 'mock_user_modified@test.com',
            'last_name': 'ck_mod',
        }),
        pytest.param('temp_mock_user', {
            'username': 'mock_user_modified',
            'email': 'mock_user_modified@test.com',
            'first_name': 'mo_mod',
            'last_name': 'ck_mod',
            'role': ROLES.VISITOR,
        },)
    ],
    'test_validation': [
        pytest.param({'email': 'Abc.example.com'}, ValidationError, r'Email .* is not valid', id='email__error'),
        pytest.param({'email': 'test@test.com', 'username': 'a'}, ValidationError, r'Username .* is not valid.',
                     id='username_error'),
        pytest.param({'email': 'test@test.com', 'username': 'valid_user', 'first_name': 'a' * 151}, ValidationError,
                     r'Name .* is longer than .* letters', id='first_name_error'),
        pytest.param(
            {'email': 'test@test.com', 'username': 'valid_user', 'first_name': 'a' * 150, 'last_name': 'a' * 151},
            ValidationError, r'Name .* is longer than .* letters', id='first_name_error'),
        pytest.param(
            {'email': 'test@test.com', 'username': 'valid_user', 'first_name': 'a' * 150, 'last_name': 'a' * 150,
             'role': ROLES.VISITOR}, None, None, id='user_normal'),
    ],
    'test_get_model': [
        pytest.param(None, {
            'username': 'non_existed_user',
            'email': 'non_existed_user@test.com',
            'first_name': 'no_mo',
            'last_name': 'no_ck',
            'role': ROLES.VISITOR,
        }, False, False, AssertionError, 'Cannot make new model without validations!',
                     id='no_validate_no_model_assertion_err'),
        pytest.param('stored_mock_user', {
            'first_name': 'mo_mod',
            'last_name': 'ck_mod',
            'role': ROLES.TRANSLATOR,
        }, False, False, AssertionError, 'Cannot overwrite model without validations!',
                     id='no_validate_cant_overwrite_err', marks=pytest.mark.skip(reason='api change')),
        pytest.param(None, {
            'email': 'get_new_user@email.com',
            'username': 'get_new_user',
            'first_name': 'get_ne',
            'last_name': 'w_user',
            'role': ROLES.VISITOR,
        }, True, True, None, None, id='make_new_model'),
        pytest.param('stored_mock_user', {
            'username': 'mock_user_modified',
            'email': 'mock_user_modified@test.com',
            'last_name': 'ck_mod',
        }, True, False, None, None, id='overwrite_model'),
    ]
}, default_params={
    'first_name': '',
    'last_name': ''
})
