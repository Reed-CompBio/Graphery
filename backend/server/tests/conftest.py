from typing import Callable, Sequence

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
    def _model_factory(model_maker: Callable, model_destructor: Callable = lambda *args: None) -> Sequence[Model]:
        with django_db_blocker.unblock():
            models = model_maker()

        return models

    return _model_factory
