from typing import List, Tuple, Type

from prompt_toolkit import print_formatted_text

from cli_utils.cli_ui import run_interruptable_checkbox_dialog, new_session
from cli_utils.command_helpers.code_and_exec_result_creator import CodeExecCreator
from cli_utils.command_helpers.command_base import CommandBase
from cli_utils.command_helpers.graph_content_creator import GraphContentCreator
from cli_utils.command_helpers.graph_creator import GraphCreator
from cli_utils.command_helpers.tutorial_anchor_creator import TutorialAnchorCreator
from cli_utils.command_helpers.tutorial_content_creator import TutorialContentCreator
from cli_utils.command_helpers.user_creator import UserCreator


class CommandWrapper:
    action_values: List[Tuple[Type[CommandBase], str]] = [
        (UserCreator, 'Create User'),
        (TutorialAnchorCreator, 'Create Tutorial Anchor'),
        (TutorialContentCreator, 'Create Tutorial Content From Markdown Files'),
        (GraphCreator, 'Create Graph From Jsons'),
        (GraphContentCreator, 'Create Graph Info Content From Markdown Files'),
        (CodeExecCreator, 'Create Code and Execution Result Records')
    ]

    # TODO use instance instead of class, so that I can have a recent create list.
    @classmethod
    @new_session('create')
    def create(cls):
        action_choices: List[Type] = run_interruptable_checkbox_dialog(
            text='Please choose what you want to do',
            values=cls.action_values
        )

        for action_class in action_choices:
            action_class()()

    @staticmethod
    def add():
        print_formatted_text('Please use the admin site')

    @staticmethod
    def modify():
        print_formatted_text('Please use the admin site')

    @classmethod
    def run_command(cls, command: str) -> None:
        getattr(cls, command)()
