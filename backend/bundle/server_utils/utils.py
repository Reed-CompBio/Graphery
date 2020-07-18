import argparse
import sys
from typing import Mapping, Any

from server_utils.params import DEFAULT_PORT


def valid_version():
    v = sys.version_info
    if v.major == 3 and v.minor >= 8:
        return True
    print('Your current python is %d.%d. Please use Python 3.8.' % (v.major, v.minor))
    return False


def arg_parser() -> Mapping[str, int]:
    parser = argparse.ArgumentParser(description='Graphery Local Server')
    parser.add_argument('-p', '--port',
                        default=DEFAULT_PORT,
                        type=int,
                        help='The port the local server will run on')

    args: argparse.Namespace = parser.parse_args()
    return vars(args)


def create_error_response(message: str) -> dict:
    return {
        'errors': [{
            'message': message
        }]
    }


def create_data_response(data: Any) -> dict:
    return {
        'data': data if isinstance(data, Mapping) else {'info': data}
    }
