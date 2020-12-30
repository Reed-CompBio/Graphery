from uuid import UUID

import pytest

from backend.intel_wrappers.intel_wrapper import UserWrapper
from backend.intel_wrappers.validators import ValidationError
from backend.model.UserModel import ROLES
from tests.wrapper_test.test_wrapper_helper import gen_wrapper_test_class


# for pycharm quick start 
class TestUserWrapper:
    def test_func(self):
        pass


TestUserWrapper = gen_wrapper_test_class(wrapper_class=UserWrapper, test_params={
    'test_load': [
        ('mock_user', True),
        ('mock_user', False)
    ],
    'test_set_variables': [
        {
            'email': 'set_user@email.com',
            'username': 'set_user',
            'first_name': 'set',
            'last_name': 'user',
            'role': ROLES.VISITOR,
        },
        {
            'email': 'set_user@email.com',
            'last_name': 'user',
            'role': ROLES.VISITOR,
        },
        {
            'last_name': 'user',
        }
    ],
    'test_making_new_model': [
        {
            'email': 'new_user@email.com',
            'username': 'new_user',
            'first_name': 'new',
            'last_name': 'user',
            'role': ROLES.VISITOR,
        }
    ],
    'test_retrieve_model': [
        pytest.param('mock_user', {'username': 'mock_user', }, marks=pytest.mark.xfail),
        pytest.param('mock_user', {'email': 'mock_user@test.com', }, marks=pytest.mark.xfail),
        pytest.param('mock_user', {'username': 'mock_user', 'email': 'mock_user@test.com', }),
    ],
    'test_overwrite': [
        pytest.param('mock_user', {'username': 'mock_user_modified'}, UUID('96e65d54-8daa-4ba0-bf3a-1169acc81b59')),
        pytest.param('mock_user', {'username': 'mock_user_modified',
                                   'email': 'mock_user_modified@test.com',
                                   'last_name': 'ck_mod',
                                   },
                     UUID('96e65d54-8daa-4ba0-bf3a-1169acc81b59')),
        pytest.param('mock_user', {'username': 'mock_user_modified',
                                   'email': 'mock_user_modified@test.com',
                                   'first_name': 'mo_mod',
                                   'last_name': 'ck_mod',
                                   'role': ROLES.VISITOR,
                                   },
                     UUID('96e65d54-8daa-4ba0-bf3a-1169acc81b59'))
    ],
    'test_validation': [
        pytest.param({'email': 'Abc.example.com'}, ValidationError, r'Email .* is not valid', id='email__error'),
        pytest.param({'email': 'test@test.com', 'username': 'a'}, ValidationError, r'Username .* is not valid.',
                     id='username_error'),
        pytest.param({'email': 'test@test.com', 'username': 'valid_user', 'first_name': 'a' * 151}, ValidationError,
                     r'Name .* is longer than .* letters', id='first_name_error'),
        pytest.param({'email': 'test@test.com', 'username': 'valid_user', 'first_name': 'a' * 150, 'last_name': 'a' * 151},
                     ValidationError, r'Name .* is longer than .* letters', id='first_name_error'),
        pytest.param({'email': 'test@test.com', 'username': 'valid_user', 'first_name': 'a' * 150, 'last_name': 'a' * 150, 'role': ROLES.VISITOR}, None, None, id='user_normal'),
    ],
    'test_get_model': [

    ]
})
