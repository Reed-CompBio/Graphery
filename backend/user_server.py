#!/usr/bin/env python3
from bundle.server_utils.utils import arg_parser, valid_version
from bundle.server_utils.main_functions import main

if __name__ == '__main__':
    if not valid_version():
        exit(1)

    try:
        main(arg_parser()['port'])
    except KeyboardInterrupt:
        print('Interrupted by keyboard.')
    except Exception as exc:
        print(f'Unknown exception occurred. Error: {exc}')
    finally:
        print('Stopped the server.')
