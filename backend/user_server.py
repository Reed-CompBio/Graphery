#!/usr/bin/env python3

import sys


def valid_version() -> bool:
    v = sys.version_info
    if v.major == 3 and v.minor >= 7:
        return True
    print('Your current python is %d.%d. Please use Python 3.7.' % (v.major, v.minor))
    return False


if not valid_version():
    exit(1)

try:
    from typing import Mapping
    from bundle.server_utils.utils import arg_parser
    from bundle.server_utils.main_functions import run_server
except Exception as e:
    print('Cannot import required packages. Error %s' % e)
    exit(1)


if __name__ == '__main__':

    args = arg_parser()
    server_url: str = args.get('url')
    server_port: int = args.get('port')
    compile_content = args.get('compile')

    try:
        if compile_content is not None and isinstance(compile_content, Mapping):
            raise NotImplementedError('CLI Compiling is not supported yet!')
        elif server_port is not None and isinstance(server_port, int):
            run_server(server_url, server_port)
        else:
            raise ValueError('Invalid Arguments')
    except KeyboardInterrupt:
        print()
        print('Interrupted by keyboard.')
    except Exception as exc:
        print(f'Unknown exception occurred. Error: {exc}')
    finally:
        print('Stopped the server.')
