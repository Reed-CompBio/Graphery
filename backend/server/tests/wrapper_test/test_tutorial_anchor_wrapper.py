from uuid import UUID

import pytest

from backend.intel_wrappers.intel_wrapper import TutorialAnchorWrapper
from backend.intel_wrappers.validators import ValidationError
from tests.wrapper_test.factories import category_wrappers_factory
from tests.wrapper_test.test_wrapper_helper import gen_wrapper_test_class


# for pycharm quick start
class TestTutorialAnchorWrapper:
    def test_func(self):
        pass


# noinspection PyRedeclaration
TestTutorialAnchorWrapper = gen_wrapper_test_class(wrapper_class=TutorialAnchorWrapper, test_params={
    'test_load': [
        pytest.param('stored_mock_tutorial_anchor', True),
        pytest.param('stored_mock_tutorial_anchor', False)
    ],
    'test_set_variables': [
        {
            'url': 'test-set-var',
            'name': 'test set var',
            'categories': category_wrappers_factory('temp cat {}', 1),
            'level': 101,
            'section': 0,
        },
        {
            'url': 'test-set-var',
            'name': 'test set var',
            'categories': category_wrappers_factory('temp cat {}', 10),
            'level': 101,
            'section': 0,
        },
        {
            'categories': [],
        },
        {
            'level': 101,
            'section': 0,
        },
        {
            'url': 'test-set-var',
            'name': 'test set var',
        },
        {
            'url': 'test-set-var',
            'name': 'test set var',
            'level': 101,
            'section': 0,
        },
        {

        }
    ],
    'test_making_new_model': [
        pytest.param({
            'url': 'test-make-new-model',
            'name': 'test make new model',
            'categories': category_wrappers_factory('make new model {}', 1),
            'level': 101,
            'section': 0,
        }),
        pytest.param({
            'url': 'test-make-new-model',
            'name': 'test make new model',
            'categories': category_wrappers_factory('test making new {}', 10),
            'level': 101,
            'section': 0,
        }),
        pytest.param({
            'url': 'test-make-new-model',
            'name': 'test make new model',
            'categories': None,
            'level': 101,
            'section': 0,
        }),
    ],
    'test_retrieve_model': [
        pytest.param('stored_mock_tutorial_anchor', {'id': UUID('b0015ac8-5376-4b99-b649-6f25771dbd91'), })
    ],
    'test_overwrite': [
        pytest.param('one_time_mock_tutorial_anchor', {
            'url': 'one_time_mock_test_tutorial_mod',
            'name': 'one time mock test tutorial mode',
            'categories': category_wrappers_factory('test overwrite {}', 5),
            'section': 2,
            'level': 222,
            'is_published': False
        }),
        pytest.param('one_time_mock_tutorial_anchor', {
            'url': 'one_time_mock_test_tutorial_mod',
            'name': 'one time mock test tutorial mode',
            'categories': [],
            'section': 2,
            'level': 222,
            'is_published': False
        }),
        pytest.param('one_time_mock_tutorial_anchor', {
            'categories': category_wrappers_factory('test overwrite cat only {}', 7)
        }),
        pytest.param('one_time_mock_tutorial_anchor', {
            'url': 'one_time_mock_test_tutorial_mod',
            'name': 'one time mock test tutorial mode',
            'categories': [],
            'section': 1,
            'level': 212,
            'is_published': True
        }),
        pytest.param('one_time_mock_tutorial_anchor', {
            'section': 1,
            'level': 212,
        }),
        pytest.param('one_time_mock_tutorial_anchor', {
            'url': 'one_time_mock_test_tutorial_mod',
            'name': 'one time mock test tutorial mode',
            'is_published': True
        }),
        pytest.param('one_time_mock_tutorial_anchor', {

            }
        )
    ],
    'test_validation': [
        pytest.param({'url': ''}, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': ''}, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': '', 'categories': None}, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': '', 'categories': [], 'level': ''}, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': '', 'categories': [], 'level': 100, 'section': 1}, ValidationError,
                     None)
    ],
    'test_get_model': [
        pytest.param(None, {
            'url': 'one_time_mock_test_tutorial_mod',
            'name': 'one time mock test tutorial mode',
            'categories': [],
            'section': 2,
            'level': 222,
            'is_published': False
        }, False, False, AssertionError, 'Cannot make new model without validations!'),
        pytest.param(None, {
            'url': 'one-time-mock-test-tutorial-mod',
            'name': 'one time mock test tutorial mode',
            'categories': [],
            'section': 2,
            'level': 222,
            'is_published': False
        }, True, True, None, None, id='make new model'),
        pytest.param('stored_mock_tutorial_anchor', {
            'id': UUID('b0015ac8-5376-4b99-b649-6f25771dbd91'),
            'url': 'mock-test-tutorial',
            'name': 'mock test tutorial',
            'section': 1,
            'level': 210,
            'is_published': True
        }, True, False, None, None, id='get old model')
    ],
    'test_finalize': [
        pytest.param('one_time_mock_tutorial_anchor', {
            'url': 'finalize-test-tutorial',
            'name': 'finalize test tutorial',
            'categories': category_wrappers_factory('full mod finalize {}', 5),
            'section': 3,
            'level': 220,
            'is_published': False
        }, True, True, None, None),
        pytest.param('one_time_mock_tutorial_anchor', {
            'url': 'finalize-test-tutorial',
            'name': 'finalize test tutorial',
            'section': 1,
            'level': 212,
            'is_published': False
        }, True, False, None, None),
        pytest.param('one_time_mock_tutorial_anchor', {
            'url': 'finalize-test-tutorial',
            'name': 'finalize test tutorial',
            'categories': []
        }, True, True, None, None),
        pytest.param('one_time_mock_tutorial_anchor', {
            'url': ''
        }, True, True, ValidationError, None),
        pytest.param(None, {
            'url': 'finalize-mock-test-tutorial',
            'name': 'finalize mock test tutorial',
            'categories': category_wrappers_factory('finalize cat {}', 7),
            'section': 1,
            'level': 213,
            'is_published': True
        }, True, True, None, None),
        pytest.param(None, {
            'url': 'finalize-mock-test-tutorial',
            'name': 'finalize mock test tutorial',
            'categories': category_wrappers_factory('finalize cat {}', 10),
            'section': 1,
            'level': 213,
        }, True, True, None, None),
        pytest.param(None, {
            'url': 'finalize-mock-test-tutorial',
            'name': 'finalize mock test tutorial',
            'categories': [],
            'section': 1,
            'level': 213,
            'is_published': True
        }, False, True, AssertionError, None),
        pytest.param(None, {
            'url': 'finalize-mock-test-tutorial',
            'name': 'finalize mock test tutorial',
            'categories': [],
            'section': 1,
            'level': 213,
            'is_published': True
        }, True, False, AssertionError, None),
    ]
}, default_params={'is_published': False})
