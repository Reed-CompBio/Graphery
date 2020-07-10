import argparse
from typing import Mapping


commands = [
    'create',
    'add',
    'modify',
]
#
# contents = [
#     'user',
#     'tutorial_anchor',
#     'tutorial_contents',
#     'graph',
#     'graph_contents',
#     'code_and_exec_records'
# ]


def arg_parser() -> Mapping[str, str]:
    parser = argparse.ArgumentParser(description='Graphery CLI')
    command_group = parser.add_argument_group('Commands')
    command_group.add_argument('command', choices=commands)
    # command_group.add_argument('content', choices=contents)

    args: argparse.Namespace = parser.parse_args()
    return vars(args)
