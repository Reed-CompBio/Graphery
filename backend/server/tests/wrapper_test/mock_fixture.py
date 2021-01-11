import os
import pathlib
from uuid import UUID

import pytest
from django.conf import settings
from django.core.files import File

from backend.model.TutorialRelatedModel import Category, Tutorial, Graph, GraphPriority, Code, ExecResultJson, Uploads
from backend.model.UserModel import User, ROLES


@pytest.fixture(scope='session')
def stored_mock_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        u = User.objects.create(**{
            'id': UUID('96e65d54-8daa-4ba0-bf3a-1169acc81b59'),
            'username': 'mock_user',
            'email': 'mock_user@test.com',
            'password': 'password',  # omitted since the password field is a encrypted version of it
            'first_name': 'mo',
            'last_name': 'ck',
            'role': ROLES.AUTHOR,
        })
    return u


@pytest.fixture()
def one_time_mock_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        u = User.objects.create(**{
            'id': UUID('c3ab4052-4188-404b-a1a5-1dc7ce5112f7'),
            'username': 'one_time_user',
            'email': 'one-time-user@test.com',
            'password': 'password',  # omitted since the password field is a encrypted version of it
            'first_name': 'one',
            'last_name': 'time',
            'role': ROLES.VISITOR,
        })

    yield u

    with django_db_blocker.unblock():
        u.delete()


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


@pytest.fixture(scope='session')
def stored_mock_category(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        c = Category.objects.create(**{
            'id': UUID('a58912ae-0343-4827-9dc1-b8518faf13ff'),
            'category': 'mock_category',
            'is_published': True
        })

    return c


@pytest.fixture()
def one_time_mock_category(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        c = Category.objects.create(**{
            'id': UUID('c7b36800-f84f-4b3b-9077-6b8d389445af'),
            'category': 'one_time_mock_category',
            'is_published': True
        })

    yield c

    with django_db_blocker.unblock():
        c.delete()


@pytest.fixture()
def temp_mock_category():
    return Category(**{
        'id': UUID('a58912ae-0343-4827-9dc1-b8518faf13ff'),
        'category': 'mock_category',
        'is_published': True
    })


@pytest.fixture(scope='session')
def stored_mock_tutorial_anchor(django_db_setup, django_db_blocker, stored_mock_category):
    with django_db_blocker.unblock():
        t = Tutorial.objects.create(**{
            'id': UUID('b0015ac8-5376-4b99-b649-6f25771dbd91'),
            'url': 'mock-test-tutorial',
            'name': 'mock test tutorial',
            'section': 1,
            'level': 210,
            'is_published': True
        })
        t.categories.add(stored_mock_category)
    return t


@pytest.fixture()
def one_time_mock_tutorial_anchor(django_db_setup, django_db_blocker, stored_mock_category):
    with django_db_blocker.unblock():
        t = Tutorial.objects.create(**{
            'id': UUID('98158c8f-9e57-4222-bd22-834863cfbeb6'),
            'url': 'one-time-mock-test-tutorial',
            'name': 'one time mock test tutorial',
            'section': 1,
            'level': 212,
            'is_published': True
        })
        t.categories.add(stored_mock_category)
    yield t

    with django_db_blocker.unblock():
        t.delete()


@pytest.fixture(scope='session')
def stored_mock_graph(django_db_setup, django_db_blocker,
                      stored_mock_user, stored_mock_category, stored_mock_tutorial_anchor):
    with django_db_blocker.unblock():
        g = Graph.objects.create(**{
            'id': UUID('6a831c16-903d-47d8-94ac-61d8bd419bd3'),
            'url': 'make-new-model-test-graph',
            'name': 'make nem model test graph',
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'is_published': True,
        })

        g.categories.set([stored_mock_category])
        g.authors.set([stored_mock_user])
        g.tutorials.set([stored_mock_tutorial_anchor])

    return g


@pytest.fixture()
def one_time_mock_graph(django_db_setup, django_db_blocker,
                        stored_mock_user, stored_mock_category, stored_mock_tutorial_anchor):
    with django_db_blocker.unblock():
        g = Graph.objects.create(**{
            'id': UUID('e4fa4bdc-6189-4cbc-bc7a-ab6767100cfa'),
            'url': 'make-one-time-model-test-graph',
            'name': 'make one time model test graph',
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'is_published': True,
        })

        g.categories.set([stored_mock_category])
        g.authors.set([stored_mock_user])
        g.tutorials.set([stored_mock_tutorial_anchor])

    yield g

    with django_db_blocker.unblock():
        g.delete()


@pytest.fixture(scope='session')
def stored_mock_code(django_db_setup, django_db_blocker, stored_mock_tutorial_anchor):
    with django_db_blocker.unblock():
        return Code.objects.create(**{
            'id': UUID('24d137dc-5cc2-4ace-b71c-e5b9386a2281'),
            'name': 'stored mock code',
            'tutorial': stored_mock_tutorial_anchor,
            'code': 'def hello(): \tprint("hello world!")'
        })


@pytest.fixture()
def one_time_mock_code(django_db_setup, django_db_blocker, one_time_mock_tutorial_anchor):
    with django_db_blocker.unblock():
        c = Code.objects.create(**{
            'id': UUID('8ceb0d01-cd29-4fe9-a37b-758b8e6d943c'),
            'name': 'one time mock code',
            'tutorial': one_time_mock_tutorial_anchor,
            'code': 'def hello(): \tprint("hello world!!!")'
        })

    yield c

    with django_db_blocker.unblock():
        c.delete()


@pytest.fixture(scope='session')
def stored_mock_execution_result(django_db_setup, django_db_blocker,
                                 stored_mock_code, stored_mock_graph):
    with django_db_blocker.unblock():
        return ExecResultJson.objects.create(
            **{
                'id': UUID('1b9952bf-fd26-4189-b657-8a2a982e9c23'),
                'code': stored_mock_code,
                'graph': stored_mock_graph,
                'json': {'object': 'hello world'},
                # no breakpoints for now
            }
        )


@pytest.fixture()
def one_time_mock_execution_result(django_db_setup, django_db_blocker,
                                   one_time_mock_code, one_time_mock_graph):
    with django_db_blocker.unblock():
        e = ExecResultJson.objects.create(
            **{
                'id': UUID('fd82bcc0-0886-4a56-88b8-1d3c1d110bd4'),
                'code': one_time_mock_code,
                'graph': one_time_mock_graph,
                'json': {'object': 'hello world!'},
                # no breakpoints for now
            }
        )

    yield e

    with django_db_blocker.unblock():
        e.delete()


_FILE_PATH_ROOT = pathlib.Path(settings.MEDIA_ROOT)
_STORED_TEST_FILE = _FILE_PATH_ROOT / 'stored_temp'
_ONE_TIME_TEST_FILE = _FILE_PATH_ROOT / 'one_time_temp'
_ADD_ON_TEST_FILE = _FILE_PATH_ROOT / 'add_on_temp'


@pytest.fixture(scope='session')
def stored_test_file():
    with open(_STORED_TEST_FILE, 'w+') as test_file:
        test_file.write('temp')
        yield File(test_file)

    os.remove(_STORED_TEST_FILE)


@pytest.fixture()
def one_time_test_file():
    with open(_ONE_TIME_TEST_FILE, 'w+') as test_file:
        test_file.write('temp')
        yield File(test_file)

    os.remove(_ONE_TIME_TEST_FILE)


@pytest.fixture()
def add_on_test_file():
    with open(_ADD_ON_TEST_FILE, 'w+') as test_file:
        test_file.write('temp')
        yield File(test_file)

    os.remove(_ADD_ON_TEST_FILE)


@pytest.fixture(scope='session')
def stored_uploads(django_db_setup, django_db_blocker, stored_test_file):
    with django_db_blocker.unblock():
        return Uploads.objects.create(
            id=UUID('d4c31662-2de5-44c3-af1d-bad04360dab1'),
            file=stored_test_file,
            alias='uploads store testing'
        )


@pytest.fixture()
def one_time_uploads(django_db_setup, django_db_blocker, one_time_test_file):
    with django_db_blocker.unblock():
        u = Uploads.objects.create(
            id=UUID('b6150a4e-f8bb-4f46-932d-9cb80b1279b5'),
            file=one_time_test_file,
            alias='uploads temp testing'
        )

    yield u

    with django_db_blocker.unblock():
        u.delete()
