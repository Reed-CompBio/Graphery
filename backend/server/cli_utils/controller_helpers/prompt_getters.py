import pathlib
from typing import Tuple

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator

from cli_utils.cli_ui import new_session
from cli_utils.controller_helpers.cli_validators import location_validator, path_completer


def new_line_prompt(*args, **kwargs) -> str:
    message = kwargs.pop('message', '\n') + '\n'
    return prompt(message=message, *args, **kwargs)


@new_session('input location')
def get_location(prompt_text: str = 'Please enter location',
                 validator: Validator = location_validator) -> pathlib.Path:
    return pathlib.Path(new_line_prompt(message=prompt_text,
                                        validator=validator,
                                        completer=path_completer, ))


@new_session('input name')
def get_name(message: str = '', validator: Validator = None, default: str = '') -> str:
    return new_line_prompt(message=message,
                           validator=validator,
                           default=default).strip()


@new_session('input url')
def get_url(message: str = '', validator: Validator = None, default: str = '') -> str:
    return new_line_prompt(message=message,
                           validator=validator,
                           default=default.replace(' ', '-')).strip()


@new_session('input abstract')
def get_abstract(message: str = '', validator: Validator = None, default: str = '', multiline=False) -> str:
    return new_line_prompt(message=message, validator=validator, default=default, multiline=multiline)


@new_session('input password')
def get_password(message: str = '', validator: Validator = None):
    return prompt(message=message, validator=validator, is_password=True)


@new_session('input email')
def get_email(message: str = '', validator: Validator = None):
    return prompt(message=message, validator=validator)
