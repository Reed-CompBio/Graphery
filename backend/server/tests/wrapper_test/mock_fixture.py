from uuid import UUID

import pytest

from backend.intel_wrappers.intel_wrapper import CategoryWrapper
from backend.model.TutorialRelatedModel import Category, Tutorial, Graph, GraphPriority, Code
from backend.model.UserModel import User, ROLES


@pytest.fixture(scope='module')
def stored_mock_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return User.objects.create(**{
            'id': UUID('96e65d54-8daa-4ba0-bf3a-1169acc81b59'),
            'username': 'mock_user',
            'email': 'mock_user@test.com',
            'password': 'password',  # omitted since the password field is a encrypted version of it
            'first_name': 'mo',
            'last_name': 'ck',
            'role': ROLES.AUTHOR,
        })


@pytest.fixture()
def temp_mock_user():
    return User(**{
        'id': UUID('96e65d54-8daa-4ba0-bf3a-1169acc81b59'),
        'username': 'mock_user',
        'email': 'mock_user@test.com',
        'password': 'password',  # omitted since the password field is a encrypted version of it
        'first_name': 'mo',
        'last_name': 'ck',
        'role': ROLES.AUTHOR,
    })


@pytest.fixture(scope='module')
def stored_mock_category(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return Category.objects.create(**{
            'id': UUID('a58912ae-0343-4827-9dc1-b8518faf13ff'),
            'category': 'mock_category',
            'is_published': True
        })


@pytest.fixture()
def temp_mock_category():
    return Category(**{
        'id': UUID('a58912ae-0343-4827-9dc1-b8518faf13ff'),
        'category': 'mock_category',
        'is_published': True
    })


@pytest.fixture(scope='module')
def stored_mock_tutorial_anchor(django_db_setup, django_db_blocker, stored_mock_category):
    with django_db_blocker.unblock():
        t = Tutorial.objects.create(**{
            'url': 'mock_test_tutorial',
            'name': 'mock test tutorial',
            'section': 1,
            'level': 210
        })
        t.categories.add(stored_mock_category)
    return t


@pytest.fixture()
def temp_mock_tutorial_anchor(temp_mock_category):
    t = Tutorial(**{
        'url': 'mock_test_tutorial',
        'name': 'mock test tutorial',
        'section': 1,
        'level': 210
    })

    t.categories.add(temp_mock_category)
    return t


@pytest.fixture(scope='module')
@pytest.mark.django_db
def mock_graph():
    return Graph.objects.create(**{
        'url': 'make-new-model-test-graph',
        'name': 'make nem model test graph',
        'priority': GraphPriority.MAIN,
        'cyjs': {'json': 'hello'},
    })


@pytest.fixture(scope='module')
@pytest.mark.django_db
def mock_code(mock_tutorial):
    return Code.objects.create(**{
        'tutorial': mock_tutorial,
        'code': 'def hello(): \tprint("hello world")'
    })


@pytest.fixture()
@pytest.mark.django_db
def get_fixture(request):
    def _get_fixture(name):
        return request.getfixturevalue(name)

    return _get_fixture
