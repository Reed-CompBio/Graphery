from operator import eq, ne
from typing import Type, Mapping, Callable, Optional, Sequence, Any, Tuple, Dict

import pytest
from django.db.models import Manager

from backend.intel_wrappers.wrapper_bases import AbstractWrapper
from tests.wrapper_test.factories import wrappers_to_models_helper, \
    wrapper_to_model_helper


def _apply_param_wrapper(param_string: str, param_mapping: Mapping) -> Callable:
    def _wrapper(f):
        injected_mapping = param_mapping.get(f.__name__, None)
        if injected_mapping is None:
            return pytest.mark.skip(reason='No Test Data.')(f)
        else:
            return pytest.mark.parametrize(param_string, injected_mapping)(f)

    return _wrapper


def _test_variable(django_db_blocker,
                   loaded_var: Any,
                   expected_var: Any,
                   operator: Callable,
                   manager_prepared: bool = False) -> bool:
    if isinstance(loaded_var, Sequence) and all(isinstance(wrapper, AbstractWrapper) for wrapper in loaded_var):
        for wrapper in loaded_var:
            assert operator(wrapper.model, expected_var)
    elif isinstance(loaded_var, Manager):
        # loaded_instance_var could be many-to-many fields, ForeignKey etc.
        # and in this case, the expected values are sequences

        if not manager_prepared:
            return True

        with django_db_blocker.unblock():
            # load vars from the manager
            loaded_var = list(loaded_var.all())

        # the two results should have the same length and elements
        assert operator(len(expected_var), len(loaded_var))
        for wrapper in expected_var:
            assert isinstance(wrapper, AbstractWrapper)
            assert wrapper.model in loaded_var
    else:
        if isinstance(expected_var, AbstractWrapper):
            assert operator(loaded_var, expected_var.model)
        else:
            assert operator(loaded_var, expected_var)

    return True


def test_variable_equality(django_db_blocker,
                           loaded_var: Any,
                           expected_var: Any,
                           manager_prepared: bool = False) -> bool:
    return _test_variable(django_db_blocker, loaded_var, expected_var, eq, manager_prepared)


def test_variable_non_equality(django_db_blocker,
                               loaded_var: Any,
                               expected_var: Any,
                               manager_prepared: bool = False) -> bool:
    return _test_variable(django_db_blocker, loaded_var, expected_var, ne, manager_prepared)


def is_wrappers_factory_tuple(value: Any) -> bool:
    return isinstance(value, Tuple) and len(value) == 2 \
           and all(hasattr(item, '__name__') for item in value) and \
           value[0].__name__.endswith('_ws_maker') and value[1].__name__.endswith('_ws_destructor')


def is_wrapper_factory_tuple(value: Any) -> bool:
    return isinstance(value, Tuple) and len(value) == 2 \
           and all(hasattr(item, '__name__') for item in value) and \
           value[0].__name__.endswith('_w_maker') and value[1].__name__.endswith('_w_destructor')


def get_actual_value(value: Any, factory_maker: Callable, wrappers_to_models: bool, wrapper_to_model: bool) -> Any:
    if is_wrappers_factory_tuple(value):
        return wrappers_to_models_helper(factory_maker(*value)) if wrappers_to_models else factory_maker(*value)
    elif is_wrapper_factory_tuple(value):
        return wrapper_to_model_helper(factory_maker(*value)) if wrapper_to_model else factory_maker(*value)
    return value


def remake_input_mapping(mapping: Dict, factory_maker: Callable,
                         wrappers_to_models: bool = False, wrapper_to_model: bool = False) -> Dict:
    for key, value in mapping.items():
        mapping[key] = get_actual_value(value, factory_maker, wrappers_to_models, wrapper_to_model)

    return mapping


def gen_wrapper_test_class(wrapper_class: Type[AbstractWrapper],
                           test_params: Mapping,
                           default_params: Mapping = None) -> Type:
    if default_params is None:
        default_params = {}

    def apply_param_wrapper(arg_list_str: str) -> Callable:
        return _apply_param_wrapper(arg_list_str, test_params)

    # noinspection PyArgumentList
    class TestWrapper:
        wrapper_type: Type[AbstractWrapper] = wrapper_class
        default_args: Mapping = default_params

        @apply_param_wrapper('mock_instance_name, load_var')
        def test_load(self, get_fixture, django_db_blocker,
                      mock_instance_name: str, load_var: bool):
            model_instance = get_fixture(mock_instance_name)

            if load_var:
                with django_db_blocker.unblock():
                    model_wrapper = self.wrapper_type().load_model(model_instance, load_var=load_var)
            else:
                model_wrapper = self.wrapper_type().load_model(model_instance, load_var=load_var)

            # TODO user fixture to test loading
            assert model_wrapper.model is not None and model_wrapper.model == model_instance
            if load_var:
                for key in model_wrapper.validators.keys():
                    field_value = getattr(model_wrapper, key)
                    loaded_var = getattr(model_instance, key)
                    test_variable_equality(django_db_blocker=django_db_blocker,
                                           loaded_var=loaded_var,
                                           expected_var=field_value,
                                           manager_prepared=True)

        @apply_param_wrapper('variable_dict')
        def test_set_variables(self, django_db_blocker, model_factory, variable_dict: Dict):
            remake_input_mapping(variable_dict, model_factory, wrappers_to_models=True, wrapper_to_model=True)

            model_wrapper = self.wrapper_type()
            model_wrapper.set_variables(**variable_dict)
            for key in model_wrapper.validators.keys():
                loaded_value = getattr(model_wrapper, key)

                if key in variable_dict:
                    expected_var = variable_dict[key]
                    test_variable_equality(django_db_blocker=django_db_blocker,
                                           loaded_var=loaded_value,
                                           expected_var=expected_var)
                elif key in self.default_args:
                    expected_var = self.default_args[key]
                    test_variable_equality(django_db_blocker=django_db_blocker,
                                           loaded_var=loaded_value,
                                           expected_var=expected_var)
                else:
                    assert loaded_value is None

        @apply_param_wrapper('init_params')
        def test_making_new_model(self, django_db_setup, django_db_blocker, model_factory,
                                  init_params: Dict):
            remake_input_mapping(init_params, model_factory)

            model_wrapper = self.wrapper_type().set_variables(**init_params)
            assert model_wrapper.model is None
            with django_db_blocker.unblock():
                model_wrapper.make_new_model()

            assert model_wrapper.model is not None
            created_model = model_wrapper.model
            for key in model_wrapper.validators.keys():
                # since id doesn't exist before the model is created
                if key != 'id':
                    loaded_instance_var = getattr(created_model, key)
                    if key in init_params:
                        expected_value = init_params[key]
                    elif key in self.default_args:
                        expected_value = self.default_args[key]
                    else:
                        # which should never happen
                        raise Exception(f'bad testing suit: mysterious key {key}')
                    test_variable_equality(django_db_blocker=django_db_blocker,
                                           loaded_var=loaded_instance_var,
                                           expected_var=expected_value)
            with django_db_blocker.unblock():
                # the object is created but not injected to db
                assert self.wrapper_type.model_class.objects.filter(id=created_model.id).count() == 0

        @apply_param_wrapper('mock_instance_name, required_info')
        def test_retrieve_model(self, get_fixture, django_db_setup, django_db_blocker, model_factory,
                                mock_instance_name: str, required_info: Dict):
            remake_input_mapping(required_info, model_factory)

            model_instance = get_fixture(mock_instance_name)
            model_wrapper = self.wrapper_type().set_variables(**required_info)
            with django_db_blocker.unblock():
                model_wrapper.retrieve_model()
            test_variable_equality(django_db_blocker=django_db_blocker,
                                   loaded_var=model_wrapper.model,
                                   expected_var=model_instance,
                                   manager_prepared=True)

        @apply_param_wrapper('mock_instance_name, modified_fields')
        def test_overwrite(self, get_fixture, django_db_blocker, model_factory,
                           mock_instance_name: str, modified_fields: Dict):
            remake_input_mapping(modified_fields, model_factory)

            model_instance = get_fixture(mock_instance_name)

            with django_db_blocker.unblock():
                model_wrapper = self.wrapper_type().load_model(model_instance).set_variables(**modified_fields)
                model_wrapper.overwrite_model()

            stored_model = model_wrapper.model

            for key in model_wrapper.validators.keys():
                loaded_value = getattr(stored_model, key)

                if key in modified_fields:
                    expected_value = modified_fields[key]
                else:
                    expected_value = getattr(model_wrapper, key)

                test_variable_equality(django_db_blocker=django_db_blocker,
                                       loaded_var=loaded_value,
                                       expected_var=expected_value,
                                       manager_prepared=True)

        @apply_param_wrapper('init_params, expected_error, error_text_match')
        def test_validation(self, model_factory,
                            init_params: Dict, expected_error: Optional[Type[Exception]], error_text_match: str):
            remake_input_mapping(init_params, model_factory)

            model_wrapper = self.wrapper_type().set_variables(**init_params)

            if expected_error is None:
                model_wrapper.validate()
            else:
                with pytest.raises(expected_error, match=error_text_match):
                    model_wrapper.validate()

        @apply_param_wrapper('mock_instance_name, init_params, validate, is_new_model, '
                             'expected_error, error_text_match')
        def test_get_model(self, get_fixture, django_db_blocker, model_factory,
                           mock_instance_name: Optional[str], init_params: Optional[Dict],
                           validate: bool, is_new_model: bool,
                           expected_error: Optional[Type[Exception]], error_text_match: str):
            if init_params is not None:
                remake_input_mapping(init_params, model_factory)

            model_wrapper = self.wrapper_type()

            if mock_instance_name is not None:
                model_instance = get_fixture(mock_instance_name)
                with django_db_blocker.unblock():
                    model_wrapper.load_model(model_instance)

            if init_params is not None:
                model_wrapper.set_variables(**init_params)

            with django_db_blocker.unblock():
                if expected_error is None:
                    new_model = model_wrapper.get_model(validate=validate)
                    assert new_model == is_new_model

                    if model_wrapper.model is not None and new_model and mock_instance_name is None:
                        model_wrapper.delete_model()
                else:
                    with pytest.raises(expected_error, match=error_text_match):
                        model_wrapper.get_model(validate=validate)

        @apply_param_wrapper('mock_instance_name, init_params, validate, overwrite, '
                             'expected_error, error_text_match')
        def test_finalize(self, django_db_blocker, get_fixture, model_factory,
                          mock_instance_name: Optional[str], init_params: Optional[Dict],
                          validate: bool, overwrite: bool,
                          expected_error: Optional[Type[Exception]], error_text_match: Optional[str]):
            if init_params is not None:
                remake_input_mapping(init_params, model_factory)

            model_wrapper = self.wrapper_type()
            original_model_wrapper = self.wrapper_type()
            no_initial_model = mock_instance_name is None
            no_init_params = init_params is None

            with django_db_blocker.unblock():
                original_count = self.wrapper_type.model_class.objects.all().count()

            if not no_initial_model:
                original_model = model_instance = get_fixture(mock_instance_name)

                with django_db_blocker.unblock():
                    model_wrapper.load_model(model_instance)
                    original_model_wrapper.load_model(original_model)

            if not no_init_params:
                model_wrapper.set_variables(**init_params)

            if expected_error is None:
                with django_db_blocker.unblock():
                    model_wrapper.finalize_model(overwrite=overwrite, validate=validate)
                    new_count = self.wrapper_type.model_class.objects.all().count()

                if no_initial_model:
                    assert model_wrapper.model is not None
                    assert new_count == original_count + 1

                for key in model_wrapper.validators.keys():
                    with django_db_blocker.unblock():
                        loaded_var = getattr(model_wrapper.model, key)
                    expected_var = getattr(model_wrapper, key)
                    original_var = getattr(original_model_wrapper, key)

                    if key in init_params and overwrite or \
                            key == 'id' and mock_instance_name is None:
                        # overwritten values
                        test_variable_equality(django_db_blocker, loaded_var=loaded_var, expected_var=expected_var,
                                               manager_prepared=True)
                        test_variable_non_equality(django_db_blocker, loaded_var=loaded_var, expected_var=original_var)
                    else:
                        # original value
                        test_variable_equality(django_db_blocker, loaded_var=loaded_var, expected_var=original_var,
                                               manager_prepared=True)
            else:
                with pytest.raises(expected_error, match=error_text_match), django_db_blocker.unblock():
                    model_wrapper.finalize_model(overwrite=overwrite, validate=validate)

                with django_db_blocker.unblock():
                    new_count = self.wrapper_type.model_class.objects.all().count()

                if no_initial_model:
                    assert new_count == original_count
                else:
                    for key in model_wrapper.validators.keys():
                        loaded_var = getattr(model_wrapper.model, key)
                        original_var = getattr(original_model_wrapper, key)
                        test_variable_equality(django_db_blocker, loaded_var=loaded_var, expected_var=original_var,
                                               manager_prepared=True)

            if no_initial_model and model_wrapper.model is not None:
                with django_db_blocker.unblock():
                    model_wrapper.delete_model()

    return TestWrapper

#
# @pytest.fixture
# @pytest.mark.django_db
# def make_new_model_data_fixture_fixed(mock_user,
#                                       mock_category,
#                                       mock_tutorial,
#                                       mock_graph,
#                                       mock_code):
#     return [
#         (UserWrapper, {
#             'username': 'make-new-model-test',
#             'email': 'test-new-model_test@test.com',
#             'role': ROLES.AUTHOR,
#         }),
#         (CategoryWrapper, {
#             'category': 'make-new-category-test',
#         }),
#         (TutorialAnchorWrapper, {
#             'url': 'make-new-model-test',
#             'name': 'make new model test',
#             'categories': [CategoryWrapper().load_model(mock_category)],
#         }),
#         (GraphWrapper, {
#             'url': 'make-new-model-test-graph',
#             'name': 'make nem model test graph',
#             'categories': [CategoryWrapper().load_model(cat) for cat in Category.objects.all()],
#             'authors': [UserWrapper().load_model(mock_user)],
#             'priority': GraphPriority.MAIN,
#             'cyjs': {'json': 'hello'},
#             'tutorials': [TutorialAnchorWrapper().load_model(tutorial) for tutorial in Tutorial.objects.all()],
#         }),
#         (CodeWrapper, {
#             'tutorial': TutorialAnchorWrapper().load_model(Tutorial.objects.get(url='cli-test')),
#             'code': 'def hello(): \tprint("hello world")'
#         }),
#         (ExecResultJsonWrapper, {
#             'code': CodeWrapper().load_model(mock_code),
#             'graph': GraphWrapper().load_model(mock_graph),
#             'json': {'json': 'hello hello'}
#         }),
#         (ENUSTutorialContentWrapper, {
#             'title': 'new-model-test',
#             'authors': [UserWrapper().load_model(model) for model in User.objects.all()],
#             'tutorial_anchor': TutorialAnchorWrapper().load_model(mock_tutorial),
#             'abstract': 'this is an abstract actually',
#             'content_md': '# hello',
#             'content_html': '<h1>hello</h1>'
#         }),
#         (ENUSGraphContentWrapper, {
#             'title': 'this is the title',
#             'abstract': 'this is the abstract :).',
#             'graph_anchor': GraphWrapper().load_model(mock_graph)
#         })
#     ]
#
# @pytest.mark.django_db
# def test_make_new_model_from_fixed_wrappers(make_new_model_data_fixture_fixed):
#     for wrapper_class, new_data in make_new_model_data_fixture_fixed:
#         make_new_model_test_helper(wrapper_class(), new_data)
#
# @pytest.fixture
# @pytest.mark.django_db
# def make_new_model_varied(mock_tutorial, mock_graph):
#     return [
#         (TutorialTranslationContentWrapper, ENUS, {
#             'title': 'new-model-test',
#             'authors': [UserWrapper().load_model(model) for model in User.objects.all()],
#             'tutorial_anchor': TutorialAnchorWrapper().load_model(mock_tutorial),
#             'abstract': 'this is an abstract actually',
#             'content_md': '# hello',
#             'content_html': '<h1>hello</h1>'
#         }),
#         (GraphTranslationContentWrapper, ENUSGraphContent, {
#             'title': 'this is the title',
#             'abstract': 'this is the abstract :).',
#             'graph_anchor': GraphWrapper().load_model(mock_graph)
#         })
#     ]
#
# @pytest.mark.django_db
# def test_make_new_model_from_varied_wrappers(make_new_model_varied):
#     for wrapper_class, wrapped_class, data in make_new_model_varied:
#         make_new_model_test_helper(wrapper_class().set_model_class(wrapped_class), data)
#
# @pytest.mark.skip(reason='API change')
# @pytest.mark.parametrize('wrapper_class, mock_fixture, changed_data', [
#     (UserWrapper, 'mock_user', {
#         'username': 'new-user-name',
#         'email': 'new-email@emai.com',
#         'password': 'new-password',
#         'role': ROLES.VISITOR,
#     }),
#     (CategoryWrapper, 'mock_category', {
#         'category': 'new-category',
#     }),
#     (TutorialAnchorWrapper, 'mock_tutorial', {
#         'url': 'new-url',
#         'name': 'new name',
#     }),
#     (GraphWrapper, 'mock_graph', {
#         'url': 'new-url-graph',
#         'name': 'new url graph',
#         'priority': GraphPriority.TRIV,
#         'cyjs': {'new': 'json'},
#     }),
#     (CodeWrapper, 'mock_code', {
#         'code': 'new code!'
#     }),
#     # TODO add exec result test
#     # TODO add relationship overwrite test
#     # ('mock_exec_result', {
#     #
#     # })
# ])
# @pytest.mark.django_db
# def test_overwrite(wrapper_class, mock_fixture, changed_data, get_fixture):
#     wrapper_instance = wrapper_class().load_model(get_fixture(mock_fixture))
#     wrapper_instance.set_variables(**changed_data)
#     wrapper_instance.prepare_model()
#     wrapper_instance.get_model()
#
#
