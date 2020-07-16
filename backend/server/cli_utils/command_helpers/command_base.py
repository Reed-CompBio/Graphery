from abc import ABC
from typing import Any,  List

from django.db.transaction import commit, rollback
from prompt_toolkit import prompt, print_formatted_text

from cli_utils.cli_ui import info_session


class CommandBase:
    def __init__(self, command_name: str):
        self.command_name: str = command_name
        self.command_attrs: dict = {}

    def set_attr(self, name: str, value: Any) -> Any:
        self.command_attrs[name] = value
        return value

    def get_attr(self, name: str) -> Any:
        return self.command_attrs[name]

    def gather_info(self) -> None:
        raise NotImplementedError

    def output_created_confirmation_info(self) -> None:
        raise NotImplementedError

    def output_not_created_confirmation_info(self) -> None:
        raise NotImplementedError

    def output_confirmation_info(self, is_created: bool) -> None:
        info_session()
        if is_created:
            self.output_created_confirmation_info()
        else:
            self.output_not_created_confirmation_info()

    def create(self) -> bool:
        raise NotImplementedError

    def proceed_helper(self) -> None:
        raise NotImplementedError

    def proceed_action(self):
        self.proceed_helper()
        commit()
        print_formatted_text('Changes committed.')

    def proceed_confirmation(self) -> None:
        proceed = prompt('Proceed Saving? (y/N) ')
        if proceed.lower() == 'y':
            self.proceed_action()
        else:
            print_formatted_text('Changes not saved. Rolling back.')
            rollback()
            print_formatted_text('Rolled back')

    def publish_confirmation(self) -> None:
        pass

    def __call__(self, overwrite: bool = False) -> None:
        # TODO catch not succeeded error and ask again?
        self.gather_info()
        is_created = self.create()
        self.output_confirmation_info(is_created)
        if is_created:
            self.proceed_confirmation()
            self.publish_confirmation()


class CommandBaseOverIterable(CommandBase, ABC):
    def __init__(self, command_name: str):
        super().__init__(command_name)
        self.command_attrs: List[dict] = []

    def set_attr(self, name: str, value: Any) -> Any:
        self.command_attrs[-1][name] = value
        return value

    def get_attr(self, name: str) -> Any:
        # TODO
        raise

    def new_attr(self) -> None:
        self.command_attrs.append({})

    def del_attr(self) -> Any:
        return self.command_attrs.pop()
