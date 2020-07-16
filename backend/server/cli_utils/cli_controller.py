import pathlib
from typing import Tuple, List, MutableMapping, Sequence

from prompt_toolkit import print_formatted_text

from backend.model.UserModel import ROLES


from bundle.GraphObjects.Graph import Graph as CustomGraph

from cli_utils.cli_ui import run_interruptable_checkbox_dialog, new_session, \
    info_session
from cli_utils.controller_helpers.cli_validators import code_source_folder_validator, email_validator, \
    password_validator, username_validator
from .controller_helpers.content_creator_helper import get_file_name_and_lang
from .controller_helpers.prompt_consent import proceed_prompt, proceed_publishing_content_iter
from .controller_helpers.prompt_getters import get_name, get_location, get_abstract, get_code_text_and_graph_req
from .controller_helpers.prompt_selectors import select_tutorial, select_graph, select_graph_lang, select_role

from .intel_wrapper import *





def create_user() -> None:
    email: str = get_email(message='Please input email: ', validator=email_validator)
    username: str = get_name(message='Please input username: ', validator=username_validator)
    role: int = select_role()
    while True:
        password: Optional[str] = enter_password()
        if password is None:
            print_formatted_text('The two do not match. Please reenter!')
        else:
            break

    user_wrapper = UserWrapper().set_variables(
        email=email,
        username=username,
        password=password,
        role=role
    )

    info_session()
    print_formatted_text('The following user will be created/overwritten: ')
    print_formatted_text(f'username: {username}')
    print_formatted_text(f'email: {email}')
    print_formatted_text(f'password: {password}')
    print_formatted_text(f'role: {ROLES(role).label}')

    def actions():
        finalize_prerequisite_wrapper(user_wrapper)

    proceed_prompt(actions=actions)


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
