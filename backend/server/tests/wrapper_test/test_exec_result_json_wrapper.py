import pytest

from backend.intel_wrappers.intel_wrapper import ExecResultJsonWrapper
from backend.intel_wrappers.validators import ValidationError
from tests.wrapper_test.factories import code_wrapper_factory, graph_wrapper_factory
from tests.wrapper_test.test_wrapper_helper import gen_wrapper_test_class


# for pycharm quick start
class TestExecResultJsonWrapper:
    def test_func(self):
        pass


# noinspection PyRedeclaration
TestExecResultJsonWrapper = gen_wrapper_test_class(wrapper_class=ExecResultJsonWrapper, test_params={
    'test_load': [
        pytest.param('stored_mock_execution_result', True),
        pytest.param('stored_mock_execution_result', False)
    ],
    'test_set_variables': [
        pytest.param({

        }, id='empty_variables'),
        pytest.param({
            'json': {'json': 'object'}
        }, id='empty_variables'),
        pytest.param({
            'code': code_wrapper_factory(
                code_name='exec test set var code',
                code_content='this is code',
                tutorial_url_template='code-set-var-url',
                tutorial_name_template='code set var url',
            )
        }),
        pytest.param({
            'code': code_wrapper_factory(
                code_name='exec test set var code',
                code_content='this is code',
                tutorial_url_template='code-set-var-url',
                tutorial_name_template='code set var url',
            ),
            'graph': graph_wrapper_factory(
                graph_url='code-tutorial-url',
                graph_name='code tutorial name',
                graph_json={'json': 'object'},
            )
        })
    ],
    'test_making_new_model': [
        {
            'graph': graph_wrapper_factory(
                graph_url='code-tutorial-url',
                graph_name='code tutorial name',
                graph_json={'json': 'object'},
            ),
            'code': code_wrapper_factory(
                code_name='exec test make new model code',
                code_content='this is code',
                tutorial_url_template='code-make-new-url',
                tutorial_name_template='code make new url',
            ),
            'json': {'json': 'object'}
        }
    ],
    # 'test_retrieve_model': [
    #     pytest.param('stored_mock_code', {'id': UUID('24d137dc-5cc2-4ace-b71c-e5b9386a2281'), }, ),
    # ],
    'test_overwrite': [
        pytest.param('one_time_mock_execution_result', {
            'graph': graph_wrapper_factory(
                graph_url='code-tutorial-url',
                graph_name='code tutorial name',
                graph_json={'json': 'object'},
            ),
            'code': code_wrapper_factory(
                code_name='exec test overwrite model code',
                code_content='this is code',
                tutorial_url_template='code-overwrite-url',
                tutorial_name_template='code overwrite',
            ),
            'json': {'json': 'object'}
        }),
        pytest.param('one_time_mock_execution_result', {
            'graph': graph_wrapper_factory(
                graph_url='code-tutorial-url',
                graph_name='code tutorial name',
                graph_json={'json': 'object'},
            ),
            'json': {'json': 'object'}
        }),
        pytest.param('one_time_mock_execution_result', {
            'code': code_wrapper_factory(
                code_name='exec test overwrite model code',
                code_content='this is code',
                tutorial_url_template='code-overwrite-url',
                tutorial_name_template='code overwrite',
            ),
            'json': {'json': 'object'}
        }),
        pytest.param('one_time_mock_execution_result', {
            'json': {'json': 'object'}
        }),
    ],
    'test_validation': [
        pytest.param({'code': None, 'graph': None, 'json': object()}, AttributeError, None,
                     id='invalid tutorial'),
        pytest.param({'code': code_wrapper_factory(
            code_name='exec test validate model code',
            code_content='this is code',
            tutorial_url_template='code-overwrite-url',
            tutorial_name_template='code overwrite',
        ), 'graph': None, 'json': object()}, AttributeError, None, id='invalid graph'),
        pytest.param({'code': code_wrapper_factory(
            code_name='exec test overwrite model code',
            code_content='this is code',
            tutorial_url_template='code-overwrite-url',
            tutorial_name_template='code overwrite',
        ), 'graph': graph_wrapper_factory(
            graph_url='code-tutorial-url',
            graph_name='code tutorial name',
            graph_json={'json': 'object'},
        ),
            'json': object()}, ValidationError, None, id='invalid json'),
    ],
    'test_get_model': [
        pytest.param(None, {
            'graph': graph_wrapper_factory(
                graph_url='code-tutorial-url',
                graph_name='code tutorial name',
                graph_json={'json': 'object'},
            ),
            'code': code_wrapper_factory(
                code_name='exec test get model code',
                code_content='this is code',
                tutorial_url_template='code-get-model-url',
                tutorial_name_template='code get model',
            ),
            'json': {'json': 'object'}
        }, False, False, AssertionError, 'Cannot make new model without validations!',
                     id='no_validate_no_model_assertion_err'),
        pytest.param(None, {
            'graph': graph_wrapper_factory(
                graph_url='code-tutorial-url',
                graph_name='code tutorial name',
                graph_json={'json': 'object'},
            ),
            'code': code_wrapper_factory(
                code_name='exec test get model code',
                code_content='this is code',
                tutorial_url_template='code-get-model-url',
                tutorial_name_template='code get model',
            ),
            'json': {'json': 'object'}
        }, True, True, None, None, id='make_new_model'),
        pytest.param('one_time_mock_execution_result', {
            'json': {'json': 'object'}
        }, True, False, None, None, id='overwrite_model'),
    ],
    'test_finalize': [
        pytest.param('one_time_mock_execution_result', {
            'json': {'json': 'object'}
        }, True, True, None, None),
        pytest.param('one_time_mock_execution_result', {
            'json': {'json': 'object'}
        }, True, False, None, None),
        pytest.param('one_time_mock_execution_result', {
            'json': object()
        }, True, True, ValidationError, None),
        pytest.param(None, {
            'graph': graph_wrapper_factory(
                graph_url='code-tutorial-url',
                graph_name='code tutorial name',
                graph_json={'json': 'object'},
            ),
            'code': code_wrapper_factory(
                code_name='exec test finalize model code',
                code_content='this is code',
                tutorial_url_template='code-finalize-model-url',
                tutorial_name_template='code finalize model',
            ),
            'json': {'json': 'object'}
        }, True, True, None, None),
        pytest.param(None, {
            'graph': graph_wrapper_factory(
                graph_url='code-tutorial-url',
                graph_name='code tutorial name',
                graph_json={'json': 'object'},
            ),
            'code': code_wrapper_factory(
                code_name='exec test finalize model code',
                code_content='this is code',
                tutorial_url_template='code-finalize-model-url',
                tutorial_name_template='code finalize model',
            ),
            'json': {'json': 'object'}
        }, False, True, AssertionError, None),
        pytest.param(None, {
            'graph': graph_wrapper_factory(
                graph_url='code-tutorial-url',
                graph_name='code tutorial name',
                graph_json={'json': 'object'},
            ),
            'code': code_wrapper_factory(
                code_name='exec test finalize model code',
                code_content='this is code',
                tutorial_url_template='code-finalize-model-url',
                tutorial_name_template='code finalize model',
            ),
            'json': {'json': 'object'}
        }, True, False, AssertionError, None),
    ]
}, default_params={'is_published': False})
