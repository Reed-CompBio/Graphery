from typing import Mapping, Union
from enum import Enum

from bundle.server_utils.utils import create_error_response


class ResponseType(Enum):
    STOPPED = 'stopped'
    WAITING = 'waiting'
    EXECUTING = 'executing'
    EXECUTED = 'executed'


def generate_status_response_mapping(message: str = None):
    return {
        'data': {
            'executing_status': message
        }
    }


def generate_respond_message(response_type: str, response_mapping: Mapping) -> Mapping:
    return {
        'type': response_type,
        **response_mapping
    }


def generate_respond_error_message(err_message: Union[Exception, str]) -> Mapping:
    return generate_respond_message(
        response_type=ResponseType.STOPPED.value,
        response_mapping=create_error_response(str(err_message))
    )
