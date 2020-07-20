import json
import os
from typing import Union, Mapping
from itertools import product

import pytest
import pathlib

from bundle.server_utils.utils import create_error_response, create_data_response, execute
from bundle.server_utils.main_functions import application_helper
from bundle.tests.user_server_tests.server_utils import Env


def test_create_error_response():
    error_message = 'error_message'
    assert create_error_response(error_message) == {
        'errors': [{
            'message': error_message
        }]
    }


@pytest.mark.parametrize('data_obj, data', [
    pytest.param({
        'exec_result': ['result']
    }, {
        'data': {
            'exec_result': ['result']
        }
    }),
    pytest.param('this is info', {
        'data': {
            'info': 'this is info'
        }
    })
])
def test_create_data_response(data_obj, data):
    assert create_data_response(data_obj) == data


resource_root_folder: pathlib.Path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))  / 'test_files'
code_resource_folder: pathlib.Path = resource_root_folder / 'code'
graph_resource_folder: pathlib.Path = resource_root_folder / 'json'


def get_code_text(code_file_name: str) -> str:
    return (code_resource_folder / code_file_name).read_text()


def get_graph_json(graph_json_file_name: str) -> dict:
    return json.loads((graph_resource_folder / graph_json_file_name).read_text())


@pytest.mark.parametrize('code_file_name, graph_json_file_name', [
    combination for combination in product(
        ['count_degree.py', 'print_edge.py', 'print_node.py'],
        ['double_node_graph.json', 'double_node_one_edge.json', 'single_node_graph.json']
    )
])
def test_execution(code_file_name: str, graph_json_file_name: Union[str, Mapping]):
    code_text = get_code_text(code_file_name)
    graph_json = get_graph_json(graph_json_file_name)
    result = execute(code_text, graph_json)
    print(result)


@pytest.mark.parametrize('env, response', [
    pytest.param(Env(REQUEST_METHOD='GET', PATH_INFO='/env'),
                 create_data_response(Env(REQUEST_METHOD='GET', PATH_INFO='/env'))),  # info page
    pytest.param(Env(REQUEST_METHOD='GET', PATH_INFO='/venv'),
                 create_error_response('Bad Request: Wrong Methods.')),  # wrong request method
    pytest.param(Env(REQUEST_METHOD='POST', PATH_INFO='/env'),
                 create_error_response('Bad Request: Wrong Methods.')),  # wrong entry point
    pytest.param(Env(REQUEST_METHOD='POST', PATH_INFO='/run').content,
                 create_error_response('No Code Snippets Embedded In The Request.')),
    pytest.param(Env(REQUEST_METHOD='POST', PATH_INFO='/run').add_content(),
                 create_error_response('No Graph Intel Embedded In The Request.'))
])
def test_server_connection(env, response):
    mock_response = application_helper(env)
    assert mock_response == response
