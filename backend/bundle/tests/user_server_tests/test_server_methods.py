import json
import os
import textwrap
import pathlib
from time import sleep
from typing import Union, Mapping, Optional, Any
from multiprocessing import Pool, TimeoutError
from itertools import product

import pytest
import requests

from bundle.server_utils.utils import create_error_response, create_data_response, execute
from bundle.server_utils.main_functions import application_helper, main
from bundle.tests.user_server_tests.server_utils import Env, FileLikeObj, generate_wsgi_input
from bundle.server_utils.params import TIMEOUT_SECONDS, DEFAULT_PORT


class AnyResp:
    def __eq__(self, other):
        return True


AnyResp = AnyResp()


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


resource_root_folder: pathlib.Path = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / 'test_files'
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


def mock_graph_json() -> dict:
    return {'elements': {'nodes': [{'data': {'id': 'v2', 'displayed': {}}, 'style': [{}]},
                                   {'data': {'id': 'v1', 'displayed': {}}, 'style': [{}]}],
                         'edges': [{'data': {'id': 'e1', 'source': 'v1', 'target': 'v2', 'displayed': {}},
                                    'style': [{}, {}]}]},
            'style': [{'selector': 'node',
                       'style': {'label': 'data(id)', 'text-valign': 'center', 'text-halign': 'center',
                                 'text-outline-color': 'white', 'text-outline-opacity': 1, 'text-outline-width': 1,
                                 'height': '10px', 'width': '10px', 'font-size': '5px', 'border-color': 'black',
                                 'border-opacity': 1, 'border-width': 1
                                 }}]}


def mock_normal_code() -> str:
    return textwrap.dedent('''\
            from bundle.seeker import tracer
            from bundle.utils.dummy_graph import graph_object
            
            
            @tracer('edge')
            def main() -> None:
                for edge in graph_object.V:
                    print(edge)
            ''')


@pytest.mark.parametrize('env, response', [
    pytest.param(Env(REQUEST_METHOD='GET', PATH_INFO='/env').content,
                 create_data_response(Env(REQUEST_METHOD='GET', PATH_INFO='/env').content)),  # info page
    pytest.param(Env(REQUEST_METHOD='GET', PATH_INFO='/venv').content,
                 create_error_response('Bad Request: Wrong Methods.')),  # wrong request method
    pytest.param(Env(REQUEST_METHOD='POST', PATH_INFO='/env').content,
                 create_error_response('Bad Request: Wrong Methods.')),  # wrong entry point
    pytest.param(Env(REQUEST_METHOD='POST', PATH_INFO='/run', CONTENT_LENGTH='1').add_content(
        {
            'wsgi.input': FileLikeObj(json.dumps({}))
        }).content,
                 create_error_response('No Code Snippets Embedded In The Request.')),  # no code
    pytest.param(Env(REQUEST_METHOD='POST', PATH_INFO='/run', CONTENT_LENGTH='1').add_content(
        {'wsgi.input': FileLikeObj(json.dumps({
            'code': textwrap.dedent('''\
                def main():
                    print('hello')
                ''')
        }))}).content,
                 create_error_response('No Graph Intel Embedded In The Request.')),  # no graph
    pytest.param(Env(REQUEST_METHOD='POST', PATH_INFO='/run', CONTENT_LENGTH='1').add_content({
        'wsgi.input': generate_wsgi_input(code=mock_normal_code(), graph=mock_graph_json())
    }).content, AnyResp),  # normal request
    pytest.param(Env(REQUEST_METHOD='POST', PATH_INFO='/run', CONTENT_LENGTH='1').add_content({
        'wsgi.input': generate_wsgi_input(code=textwrap.dedent('''\
            from time import sleep
            graph_object = {}
            
            def main() -> None:
                while True:
                    sleep(6000)        
        '''), graph=mock_graph_json())
    }).content, create_error_response(f'Timeout: Code running timed out after {TIMEOUT_SECONDS} s.')),  # timeout error
])
def test_application_helper(env, response):
    mock_response = application_helper(env)
    assert response == mock_response


# @pytest.fixture
# def local_server():
#     with Pool(1) as pool:
#         return pool.apply_async(main, args=(DEFAULT_PORT, ))
#
#
# BASE_URL = f'http://localhost:{DEFAULT_PORT}'
#
#
# @pytest.mark.parametrize('method, url, request_body, response', [
#     pytest.param('get', '/env', None, AnyResp),
#     pytest.param('post', '/run', {'code': mock_normal_code(), 'graph': mock_graph_json()}, AnyResp)
# ])
# def test_server_connection(local_server, method: str, url: str, request_body: Optional[dict], response: Any):
#     sleep(1)
#     if method == 'get':
#         resp = requests.get(BASE_URL + url)
#     elif method == 'post':
#         resp = requests.post(BASE_URL + url, data=request_body)
#     else:
#         resp = None
#
#     assert resp.status_code == 200
#     assert response == resp.json()
#
#     try:
#         local_server.get(timeout=0.1)
#     except TimeoutError:
#         print('Ended Test')
