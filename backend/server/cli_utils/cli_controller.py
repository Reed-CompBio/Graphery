from typing import List, Callable

from prompt_toolkit import print_formatted_text

from cli_utils.cli_ui import run_interruptable_checkbox_dialog, new_session


class CommandWrapper:
    action_values = [
        (create_user, 'Create User'),
        (create_tutorial_anchor, 'Create Tutorial Anchor'),
        (create_locale_md, 'Create Tutorial Content From Markdown Files'),
        (create_graph, 'Create Graph From Jsons'),
        (create_graph_content_trans, 'Create Graph Info Content From Markdown Files'),
        (create_code_obj, 'Create Code and Execution Result Records')
    ]

    # TODO use instance instead of class, so that I can have a recent create list.
    @classmethod
    @new_session('create')
    def create(cls):
        action_choices: List[Callable] = run_interruptable_checkbox_dialog(
            text='Please choose what you want to do',
            values=cls.action_values
        )

        for action in action_choices:
            action()

    @staticmethod
    def add():
        print_formatted_text('Please use the admin site')

    @staticmethod
    def modify():
        print_formatted_text('Please use the admin site')

    @classmethod
    def run_command(cls, command: str) -> None:
        getattr(cls, command)()
