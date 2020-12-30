from typing import Type, Mapping, Callable, Optional

import pytest

from backend.intel_wrappers.wrapper_bases import AbstractWrapper


def apply_param_wrapper(param_string: str, param_mapping: Mapping) -> Callable:
    def _wrapper(f):
        injected_mapping = param_mapping.get(f.__name__, None)
        if injected_mapping is None:
            return pytest.mark.skip(reason='No Test Data.')(f)
        else:
            return pytest.mark.parametrize(param_string, injected_mapping)(f)

    return _wrapper


def gen_wrapper_test_class(wrapper_class: Type[AbstractWrapper], test_params: Mapping, default_params: Mapping = {}) -> Type:
    # noinspection PyArgumentList
    class TestWrapper:
        wrapper_type: Type[AbstractWrapper] = wrapper_class
        default_args: Mapping = default_params

        @apply_param_wrapper('mock_instance_name, load_var', test_params)
        def test_load(self, get_fixture,
                      mock_instance_name: str, load_var: bool):
            model_instance = get_fixture(mock_instance_name)
            model_wrapper = self.wrapper_type().load_model(model_instance)

            # TODO user fixture to test loading
            assert model_wrapper.model is not None and model_wrapper.model == model_instance
            if load_var:
                for key in model_wrapper.validators.keys():
                    field_value = getattr(model_wrapper, key)
                    expected_value = getattr(model_instance, key)
                    assert field_value == expected_value

        @apply_param_wrapper('variable_dict', test_params)
        def test_set_variables(self, variable_dict: Mapping):
            model_wrapper = self.wrapper_type()
            model_wrapper.set_variables(**variable_dict)
            for key in model_wrapper.validators.keys():
                loaded_value = getattr(model_wrapper, key)

                if key in variable_dict:
                    assert loaded_value == variable_dict[key]
                elif key in self.default_args:
                    assert loaded_value == self.default_args[key]
                else:
                    assert loaded_value is None

        @apply_param_wrapper('init_params', test_params)
        @pytest.mark.django_db
        def test_making_new_model(self, init_params: Mapping):
            model_wrapper = self.wrapper_type().set_variables(**init_params)
            assert model_wrapper.model is None
            model_wrapper.make_new_model()
            assert model_wrapper.model is not None
            created_model = model_wrapper.model
            for key in model_wrapper.validators.keys():
                # since id doesn't exist before the model is created
                if key != 'id':
                    injected_value = getattr(created_model, key)
                    expected_value = init_params[key]
                    assert injected_value == expected_value
            # the object is created but not injected to db
            assert self.wrapper_type.model_class.objects.filter(id=created_model.id).count() == 0

        @apply_param_wrapper('mock_instance_name, required_info', test_params)
        def test_retrieve_model(self, get_fixture, django_db_setup, django_db_blocker,
                                mock_instance_name, required_info):
            model_instance = get_fixture(mock_instance_name)
            model_wrapper = self.wrapper_type().set_variables(**required_info)
            with django_db_blocker.unblock():
                model_wrapper.retrieve_model()
            assert model_wrapper.model == model_instance

        @apply_param_wrapper('mock_instance_name, modified_fields', test_params)
        def test_overwrite(self, get_fixture,
                           mock_instance_name: str, modified_fields: Mapping):
            model_instance = get_fixture(mock_instance_name)
            model_wrapper = self.wrapper_type().load_model(model_instance).set_variables(**modified_fields)
            model_wrapper.overwrite_model()
            stored_model = model_wrapper.model

            for key in model_wrapper.validators.keys():
                injected_value = getattr(stored_model, key)

                if key in modified_fields:
                    assert injected_value == modified_fields[key]
                else:
                    assert injected_value == getattr(model_wrapper, key)

        @apply_param_wrapper('init_params, expected_error, error_text_match', test_params)
        def test_validation(self, init_params: Mapping, expected_error: Optional[Type[Exception]],
                            error_text_match: str):
            model_wrapper = self.wrapper_type().set_variables(**init_params)

            if expected_error is None:
                model_wrapper.validate()
            else:
                with pytest.raises(expected_error, match=error_text_match):
                    model_wrapper.validate()

        @apply_param_wrapper('mock_instance_name, init_params, overwrite, validate, expected_error, error_text_match',
                             test_params)
        def test_get_model(self, get_fixture, django_db_blocker,
                           mock_instance_name: Optional[str], init_params: Optional[Mapping], overwrite: bool,
                           validate: bool, expected_error: Optional[Type[Exception]], error_text_match: str):
            model_wrapper = self.wrapper_type()

            if mock_instance_name is not None:
                model_instance = get_fixture(mock_instance_name)
                model_wrapper.load_model(model_instance)

            if init_params is not None:
                model_wrapper.set_variables(**init_params)

            with django_db_blocker.unblock():
                if expected_error is None:
                    model_wrapper.get_model(overwrite=overwrite, validate=validate)
                else:
                    with pytest.raises(expected_error, match=error_text_match):
                        model_wrapper.get_model(overwrite=overwrite, validate=validate)

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
