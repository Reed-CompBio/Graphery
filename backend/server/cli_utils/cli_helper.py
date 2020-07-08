import argparse
from typing import Mapping


commands = [
    'create',
    'add',
    'modify',
]


def arg_parser() -> Mapping[str, str]:
    parser = argparse.ArgumentParser(description='Graphery CLI')
    command_group = parser.add_argument_group('Commands')
    command_group.add_argument('command', choices=commands)

    args: argparse.Namespace = parser.parse_args()
    return vars(args)
