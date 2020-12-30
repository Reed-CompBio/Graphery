from uuid import UUID

import pytest

from backend.model.TutorialRelatedModel import Category, Tutorial, Graph, GraphPriority, Code
from backend.model.UserModel import User, ROLES


@pytest.fixture(scope='module')
def mock_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return User.objects.create(**{
            'id': UUID('96e65d54-8daa-4ba0-bf3a-1169acc81b59'),
            'username': 'mock_user',
            'email': 'mock_user@test.com',
            'password': 'password',  # omitted since the password field is a encrypted version of it
            'role': ROLES.AUTHOR,
        })


@pytest.fixture(scope='module')
@pytest.mark.django_db
def mock_category():
    return Category.objects.create(**{
        'category': 'mock_category',
    })


@pytest.fixture(scope='module')
@pytest.mark.django_db
def mock_tutorial():
    return Tutorial.objects.create(**{
        'url': 'mock_test_tutorial',
        'name': 'mock test tutorial',
        'level': '305'
    })


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


@pytest.fixture(scope='module')
@pytest.mark.django_db
def get_fixture(request):
    def _get_fixture(name):
        return request.getfixturevalue(name)

    return _get_fixture
