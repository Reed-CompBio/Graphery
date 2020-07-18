from typing import Sequence, Type, Union

import pytest

from django.db import models

from backend.model.TranslationModels import TranslationBase, GraphTranslationBase, ENUS, ENUSGraphContent
from backend.model.TutorialRelatedModel import Category, GraphPriority, Tutorial, Code, Graph
from backend.model.UserModel import ROLES, User
from backend.model.translation_collection import translation_table_mapping, graph_info_translation_table_mapping
from cli_utils.intel_wrappers.intel_wrapper import UserWrapper, TutorialAnchorWrapper, CategoryWrapper, GraphWrapper, \
    ExecResultJsonWrapper, CodeWrapper, TutorialTranslationContentWrapper, GraphTranslationContentWrapper, \
    VariedTypeWrapper, FixedTypeWrapper
from cli_utils.intel_wrappers.wrapper_bases import AbstractWrapper
from .utils import EmptyValue


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
    UserWrapper,
    CategoryWrapper,
    TutorialAnchorWrapper,
    GraphWrapper,
    CodeWrapper,
    ExecResultJsonWrapper,
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


def make_new_model_test_helper(wrapper_instance: AbstractWrapper, variables: dict):
    wrapper_instance = wrapper_instance.set_variables(**variables)
    wrapper_instance.make_new_model()

    assert wrapper_instance.model is not None

    for field_name, value in variables.items():
        model_field_value = getattr(wrapper_instance.model, field_name, EmptyValue)
        assert model_field_value is not None


@pytest.fixture
@pytest.mark.django_db
def make_new_model_data_fixture_fixed():
    mock_user = User.objects.create(**{
        'username': 'mock_user',
        'email': 'mock_user@test.com',
        'password': 'password',  # omitted since the password field is a encrypted version of it
        'role': ROLES.AUTHOR,
    })

    mock_category = Category.objects.create(**{
        'category': 'mock_category',
    })

    mock_tutorial = Tutorial.objects.create(**{
        'url': 'mock_test_tutorial',
        'name': 'mock test tutorial',
    })

    mock_graph = Graph.objects.create(**{
        'url': 'make-new-model-test-graph',
        'name': 'make nem model test graph',
        'priority': GraphPriority.MAIN,
        'cyjs': {'json': 'hello'},
    })

    mock_code = Code.objects.create(**{
        'tutorial': mock_tutorial,
        'code': 'def hello(): \tprint("hello world")'
    })

    return [
        (UserWrapper, {
            'username': 'make-new-model-test',
            'email': 'test-new-model_test@test.com',
            # 'password': 'password',  # omitted since the password field is a encrypted version of it
            'role': ROLES.AUTHOR,
        }),
        (CategoryWrapper, {
            'category': 'make-new-category-test',
        }),
        (TutorialAnchorWrapper, {
            'url': 'make-new-model-test',
            'name': 'make new model test',
            'categories': [CategoryWrapper().load_model(mock_category)],
        }),
        (GraphWrapper, {
            'url': 'make-new-model-test-graph',
            'name': 'make nem model test graph',
            'categories': [CategoryWrapper().load_model(cat) for cat in Category.objects.all()],
            'authors': [UserWrapper().load_model(mock_user)],
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'tutorials': [TutorialAnchorWrapper().load_model(tutorial) for tutorial in Tutorial.objects.all()],
        }),
        (CodeWrapper, {
            'tutorial': TutorialAnchorWrapper().load_model(Tutorial.objects.get(url='cli-test')),
            'code': 'def hello(): \tprint("hello world")'
        }),
        (ExecResultJsonWrapper, {
            'code': CodeWrapper().load_model(mock_code),
            'graph': GraphWrapper().load_model(mock_graph),
            'json': {'json': 'hello hello'}
        }),
    ]


@pytest.mark.django_db
def test_make_new_model_from_fixed_wrappers(make_new_model_data_fixture_fixed):
    for wrapper_class, new_data in make_new_model_data_fixture_fixed:
        make_new_model_test_helper(wrapper_class(), new_data)


@pytest.fixture
@pytest.mark.django_db
def make_new_model_varied():
    mock_tutorial = Tutorial.objects.create(**{
        'url': 'mock_test_tutorial_varied',
        'name': 'mock test tutorial_varied',
    })

    mock_graph = Graph.objects.create(**{
        'url': 'make-new-model-test-graph-varied',
        'name': 'make nem model test graph varied',
        'priority': GraphPriority.MAIN,
        'cyjs': {'json': 'hello!'},
    })

    return [
        (TutorialTranslationContentWrapper, ENUS, {
            'title': 'new-model-test',
            'authors': [UserWrapper().load_model(model) for model in User.objects.all()],
            'tutorial_anchor': TutorialAnchorWrapper().load_model(mock_tutorial),
            'abstract': 'this is an abstract actually',
            'content_md': '# hello',
            'content_html': '<h1>hello</h1>'
        }),
        (GraphTranslationContentWrapper, ENUSGraphContent, {
            'title': 'this is the title',
            'abstract': 'this is the abstract :).',
            'graph_anchor': GraphWrapper().load_model(mock_graph)
        })
    ]


@pytest.mark.django_db
def test_make_new_model_from_varied_wrappers(make_new_model_varied):
    for wrapper_class, wrapped_class, data in make_new_model_varied:
        make_new_model_test_helper(wrapper_class().set_model_class(wrapped_class), data)


def test_overwrite():
    pass
