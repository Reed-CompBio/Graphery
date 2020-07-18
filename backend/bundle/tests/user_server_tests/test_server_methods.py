from collections import Mapping
from typing import Union

import pytest

from server_utils.utils import create_error_response, create_data_response


def test_create_error_response():
    error_message = 'error_message'
    assert create_error_response(error_message) == {
        'errors': [{
            'message': error_message
        }]
    }


@pytest.mark.parametrize('data_obj, data', [
    ({
        'exec_result': ['result']
    }, {
        'data': {
            'exec_result': ['result']
        }
    }),
    ('this is info', {
        'data': {
            'info': 'this is info'
        }
    })
])
def test_create_data_response(data_obj, data):
    assert create_data_response(data_obj) == data


def test_execute(code: str, graph_json: Union[str, Mapping]):
    pass
