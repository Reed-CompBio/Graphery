#!/usr/bin/env python3
from typing import Mapping

from server_utils.utils import arg_parser, valid_version
from server_utils.main_functions import main


def run_server(port: int) -> None:
    main(port)


if __name__ == '__main__':
    if not valid_version():
        exit(1)

    args = arg_parser()
    server_port = args.get('port', None)
    compile_content = args.get('compile', None)

    try:
        if compile_content is not None and isinstance(compile_content, Mapping):
            pass
        elif server_port is not None and isinstance(server_port, int):
            run_server(server_port)
        else:
            raise ValueError('Invalid Arguments')
    except KeyboardInterrupt:
        print()
        print('Interrupted by keyboard.')
    except Exception as exc:
        print(f'Unknown exception occurred. Error: {exc}')
    finally:
        print('Stopped the server.')
