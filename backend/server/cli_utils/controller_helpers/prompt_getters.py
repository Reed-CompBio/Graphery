import json
import pathlib
from typing import Tuple, Sequence

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator

from cli_utils.cli_ui import new_session
from cli_utils.controller_helpers.cli_validators import location_validator, path_completer, code_source_folder_validator


def strip_prompt(*args, **kwargs) -> str:
    return prompt(*args, **kwargs).strip()


def new_line_prompt(*args, **kwargs) -> str:
    message = kwargs.pop('message', '') + '\n'
    return strip_prompt(message=message, *args, **kwargs)


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
def get_password(message: str = '', validator: Validator = None) -> str:
    return strip_prompt(message=message, validator=validator, is_password=True)


@new_session('input email')
def get_email(message: str = '', validator: Validator = None) -> str:
    return strip_prompt(message=message, validator=validator)


def get_code_source_folder() -> pathlib.Path:
    return get_location(validator=code_source_folder_validator)


def get_code_text_and_graph_req(source_folder_path: pathlib.Path) -> Tuple[str, Sequence[str]]:
    json_obj = json.loads((source_folder_path / 'graph-info.json').read_text())

    if 'required_graphs' in json_obj:
        return (source_folder_path / 'entry.py').read_text(), json_obj['required_graphs']
    raise


