from typing import Sequence, Type, Union

import pytest

from django.db import models

from backend.model.TranslationModels import TranslationBase, GraphTranslationBase, ENUS, ENUSGraphContent
from backend.model.translation_collection import translation_table_mapping, graph_info_translation_table_mapping
from backend.intel_wrappers.intel_wrapper import UserWrapper, TutorialAnchorWrapper, CategoryWrapper, GraphWrapper, \
    ExecResultJsonWrapper, CodeWrapper, TutorialTranslationContentWrapper, GraphTranslationContentWrapper, \
    VariedTypeWrapper, FixedTypeWrapper, ENUSGraphContentWrapper, ZHCNTutorialContentWrapper, \
    ENUSTutorialContentWrapper, ZHCNGraphContentWrapper
from backend.intel_wrappers.wrapper_bases import AbstractWrapper
from tests.utils import EmptyValue


from django.core.management import call_command


@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_data.json')


@pytest.mark.django_db
def load_module_helper(model_instance: models.Model, module_wrapper: AbstractWrapper):
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
                   all(isinstance(field_wrapper, AbstractWrapper) for field_wrapper in field_value)

            all_models = models_field.all()
            assert all(model_wrapper.model in all_models for model_wrapper in field_value) and \
                   len(all_models) == len(field_value)

        else:
            instance_value = getattr(model_instance, field_name, EmptyValue)
            if isinstance(field_value, AbstractWrapper):
                assert instance_value == field_value.model
            else:
                assert instance_value == field_value


@pytest.mark.parametrize('wrapper_class', [
    pytest.param(UserWrapper, marks=pytest.mark.skip(reason='API change')),
    CategoryWrapper,
    TutorialAnchorWrapper,
    GraphWrapper,
    CodeWrapper,
    ExecResultJsonWrapper,
    ENUSTutorialContentWrapper,
    ZHCNTutorialContentWrapper,
    ENUSGraphContentWrapper,
    ZHCNGraphContentWrapper
])
@pytest.mark.django_db
def test_load_model_of_fixed_class_wrapper(wrapper_class: Type[FixedTypeWrapper]):
    wrapped_module_class: Type[models.Model] = wrapper_class.model_class
    assert wrapped_module_class is not None

    for model_instance in wrapped_module_class.objects.all():
        load_module_helper(model_instance, wrapper_class().load_model(model_instance))


@pytest.mark.parametrize('wrapper_class, wrapped_class', [
    *[(TutorialTranslationContentWrapper, table) for table in translation_table_mapping.values()],
    *[(GraphTranslationContentWrapper, table) for table in graph_info_translation_table_mapping.values()]
])
@pytest.mark.django_db
def test_load_model_of_trans_wrapper(wrapper_class: Type[VariedTypeWrapper],
                                     wrapped_class: Type[Union[TranslationBase, GraphTranslationBase]]):
    for model_instance in wrapped_class.objects.all():
        load_module_helper(model_instance, wrapper_class().set_model_class(wrapped_class).load_model(model_instance))


def retrieve_model_test_helper(model_instance: models.Model, wrapper_instance: AbstractWrapper):
    wrapper_instance.retrieve_model()

    assert wrapper_instance.model is not None
    assert wrapper_instance.model == model_instance


@pytest.mark.parametrize('wrapper_class', [
    UserWrapper,
    CategoryWrapper,
    TutorialAnchorWrapper,
    GraphWrapper,
    CodeWrapper,
    ExecResultJsonWrapper,
])
@pytest.mark.django_db
def test_retrieve_model_from_fixed_wrappers(wrapper_class: Type[FixedTypeWrapper]):
    wrapped_class = wrapper_class.model_class

    for model_instance in wrapped_class.objects.all():
        wrapper_instance = wrapper_class().load_model(model_instance)
        wrapper_instance.model = None
        retrieve_model_test_helper(model_instance, wrapper_instance)


@pytest.mark.parametrize('wrapper_class, wrapped_class', [
    *[(TutorialTranslationContentWrapper, table) for table in translation_table_mapping.values()],
    *[(GraphTranslationContentWrapper, table) for table in graph_info_translation_table_mapping.values()]
])
@pytest.mark.django_db
def test_retrieve_model_from_varied_wrappers(wrapper_class: Type[VariedTypeWrapper],
                                             wrapped_class: Type[Union[TranslationBase, GraphTranslationBase]]):
    for model_instance in wrapped_class.objects.all():
        wrapper_instance = wrapper_class().set_model_class(wrapped_class).load_model(model_instance)
        wrapper_instance.model = None
        retrieve_model_test_helper(model_instance, wrapper_instance)
