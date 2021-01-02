from typing import Callable, Tuple, Sequence
from uuid import UUID

import pytest

from backend.intel_wrappers.intel_wrapper import TutorialAnchorWrapper, CategoryWrapper
from backend.intel_wrappers.validators import ValidationError
from backend.model.TutorialRelatedModel import Category
from tests.wrapper_test.test_wrapper_helper import gen_wrapper_test_class


# for pycharm quick start
class TestTutorialAnchorWrapper:
    def test_func(self):
        pass


def category_wrapper_factory(template: str, num: int) -> Tuple[Callable, Callable]:
    def _maker() -> Sequence[CategoryWrapper]:
        return [
            CategoryWrapper().load_model(
                Category.objects.create(category=template.format(i))
            ) for i in range(num)
        ]

    def _destructor(category_wrappers: Sequence[CategoryWrapper]) -> None:
        for wrapper in category_wrappers:
            wrapper.delete_model()

    return _maker, _destructor


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
            'categories': [Category(category='temp cat')],
            'level': 101,
            'section': 0,
        },
        {
            'url': 'test-set-var',
            'name': 'test set var',
            'categories': [Category(category=f'temp cat {i}') for i in range(10)],
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
            'categories': [Category(category='new model cat')],
            'level': 101,
            'section': 0,
        }),
        pytest.param({
            'url': 'test-make-new-model',
            'name': 'test make new model',
            'categories': category_wrapper_factory('test making new {}', 10),
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
            'categories': category_wrapper_factory('test overwrite {}', 5),
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
        pytest.param(
            'one_time_mock_tutorial_anchor', {

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
        }, False, AssertionError, 'Cannot make new model without validations!'),
        pytest.param(None, {
            'url': 'one-time-mock-test-tutorial-mod',
            'name': 'one time mock test tutorial mode',
            'categories': [],
            'section': 2,
            'level': 222,
            'is_published': False
        }, True, None, None),
        pytest.param('stored_mock_tutorial_anchor', {
            'id': UUID('b0015ac8-5376-4b99-b649-6f25771dbd91'),
            'url': 'mock-test-tutorial',
            'name': 'mock test tutorial',
            'section': 1,
            'level': 210,
            'is_published': True
        }, True, None, None)
    ]

}, default_params={'is_published': False})
