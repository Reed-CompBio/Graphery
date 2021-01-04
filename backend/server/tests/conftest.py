from typing import Callable, Sequence, Optional, List

import pytest
from django.core.management import call_command
from django.db.models import Model


@pytest.fixture()
@pytest.mark.django_db
def get_fixture(request):
    def _get_fixture(name):
        return request.getfixturevalue(name)

    return _get_fixture


@pytest.fixture()
def model_factory(django_db_setup, django_db_blocker):
    _destructors: Optional[List[Callable]] = []

    def _model_factory(model_maker: Callable, model_destructor: Callable = lambda *args: None) -> Sequence[Model]:
        nonlocal _destructors
        assert model_maker is not None and model_destructor is not None

        with django_db_blocker.unblock():
            models = model_maker()

        _destructors.append(model_destructor)
        return models

    yield _model_factory

    for handler in _destructors:
        with django_db_blocker.unblock():
            handler()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_data.json')

