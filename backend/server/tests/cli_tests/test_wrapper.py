import os
from os.path import abspath, dirname
import pathlib
import sys
from typing import Sequence, Type

import pytest

from importlib import import_module

from django.db import models
from django import setup as django_setup

from .utils import EmptyValue


@pytest.fixture(autouse=True, scope='module')
def setup_django():
    # ehhhhhhhhhh
    sys.path.append(str(pathlib.Path(dirname(abspath(__file__))) / '../../'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphery.settings.test")
    django_setup()
    return import_module('cli_utils.intel_wrappers.intel_wrapper')


@pytest.fixture(scope='module')
def get_module():
    return import_module('cli_utils.intel_wrappers.intel_wrapper')


@pytest.fixture(scope='module')
def abstract_wrapper_type(get_module):
    return getattr(get_module, 'AbstractWrapper')


def load_module_helper(abstract_wrapper_type, model_instance: models.Model, wrapper_class: Type):
    module_wrapper = wrapper_class().load_model(model_instance)

    for field_name in module_wrapper.field_names:
        # loop through the fields in the user wrapper
        field_value = getattr(module_wrapper, field_name, EmptyValue)

        assert not isinstance(field_value, EmptyValue)

        # get the field in the model
        models_field = getattr(model_instance, field_name, EmptyValue)

        assert not isinstance(models_field, EmptyValue)

        if isinstance(models_field, models.Manager):
            # TODO sequence?
            assert isinstance(field_value, Sequence) and \
                   all(isinstance(field_wrapper, abstract_wrapper_type) for field_wrapper in field_value)

            all_models = models_field.all()
            assert all(model_wrapper.model in all_models for model_wrapper in field_value) and \
                   len(all_models) == len(field_value)

        else:
            instance_value = getattr(model_instance, field_name, EmptyValue)
            if isinstance(field_value, abstract_wrapper_type):
                assert instance_value == field_value.model
            else:
                assert instance_value == field_value


@pytest.mark.parametrize('wrapper_name', [
    'UserWrapper',
    'CategoryWrapper',
    'TutorialAnchorWrapper',
    'GraphWrapper',
    'CodeWrapper',
    'ExecResultJsonWrapper',
])
def test_load_model_of_fixed_class_wrapper(get_module, abstract_wrapper_type, wrapper_name: str):
    wrapper_class: Type[abstract_wrapper_type] = getattr(get_module, wrapper_name, EmptyValue)
    assert wrapper_class is not None

    wrapped_module_class: Type[models.Model] = wrapper_class.model_class
    assert wrapped_module_class is not None

    for model_instance in wrapped_module_class.objects.all():
        load_module_helper(abstract_wrapper_type, model_instance, wrapper_class)


def test_load_model_of_trans_wrapper():
    pass


def test_retrieve_model():
    pass


def test_make_new_model():
    pass


def test_overwrite():
    pass
