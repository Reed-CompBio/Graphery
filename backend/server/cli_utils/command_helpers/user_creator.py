from typing import Optional

from prompt_toolkit import print_formatted_text

from cli_utils.command_helpers.command_base import CommandBase
from cli_utils.controller_helpers.cli_validators import email_validator, username_validator
from cli_utils.controller_helpers.prompt_getters import get_email, get_name, enter_password
from cli_utils.controller_helpers.prompt_selectors import select_role, finalize_prerequisite_wrapper
from backend.intel_wrappers.intel_wrapper import UserWrapper


class UserCreator(CommandBase):
    def __init__(self):
        super(UserCreator, self).__init__('Create/Overwrite User')
        self.user_wrapper: Optional[UserWrapper] = None

    def gather_info(self) -> None:
        self.set_attr('email', get_email(message='Please input email: ', validator=email_validator))
        self.set_attr('username', get_name(message='Please input username: ', validator=username_validator))
        self.set_attr('role', select_role())

        while True:
            password: Optional[str] = enter_password()
            if password is None:
                print_formatted_text('The two do not match. Please reenter!')
            else:
                self.set_attr('password', password)
                break

    def output_created_confirmation_info(self) -> None:
        print_formatted_text('The following user will be created/overwritten: ')
        print_formatted_text(f'{self.user_wrapper}')

    def output_not_created_confirmation_info(self) -> None:
        print_formatted_text('No user is created')

    def create(self) -> bool:
        self.user_wrapper = UserWrapper().set_variables(**self.command_attrs)
        return True

    def proceed_helper(self) -> None:
        finalize_prerequisite_wrapper(self.user_wrapper)
