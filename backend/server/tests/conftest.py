from typing import Callable, Sequence, Any, Optional, List

import pytest
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
