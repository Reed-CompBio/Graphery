from typing import Callable, Sequence, Any, Optional

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
    _cache: Any = None
    _destructor: Optional[Callable] = None

    def _model_factory(model_maker: Callable, model_destructor: Callable = None) -> Sequence[Model]:
        nonlocal _cache, _destructor
        with django_db_blocker.unblock():
            _cache = models = model_maker()
            _destructor = model_destructor
        return models

    yield _model_factory

    if _destructor is not None:
        with django_db_blocker.unblock():
            _destructor(_cache)
