import os
import pathlib
import sys

import typing

from django.apps import apps
from django import setup as django_setup
from django.db import models

from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit import print_formatted_text
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.document import Document

import markdown


class ServerPathValidator(Validator):
    def validate(self, document: Document) -> None:
        path = pathlib.Path(document.text)
        if path.exists() and (path / 'manage.py').exists():
            pass
        else:
            raise ValidationError(
                message='The server location you provided {} is not valid'.format(str(path)),
                cursor_position=len(document.text) - 1)


class TutorialSourceFolderValidator(Validator):
    # TODO change this, store all md files in local folder
    def validate(self, document: Document) -> None:
        path = pathlib.Path(document.text)
        resource_path = (path / 'resources')
        if path.exists() and \
                resource_path.exists():
            markdown_files = [file for file in path.glob('*.md')]
            entry_py_module = resource_path / 'entry.py'
            if len(markdown_files) != 1 or not entry_py_module.exists():
                raise ValidationError(message='The tutorial source file fold must contain a markdown file '
                                              'and a `entry.py` file')

        raise ValidationError(message='The tutorial source file folder structure is not right')


prompt_session = PromptSession()
_path_completer = PathCompleter()
_server_path_validator = ServerPathValidator()
_tutorial_source_folder_validator = TutorialSourceFolderValidator()


def get_server_location() -> pathlib.Path:
    return pathlib.Path(
        prompt_session.prompt(message='Please reenter the Django server location which contains `manage.py` '
                                      'file: ',
                              validator=_server_path_validator,
                              completer=_path_completer
                              ))


def init_server_settings(server_location: pathlib.Path) -> typing.Mapping[str, models.Model]:
    # TODO this will raise exceptions
    #  django.core.exceptions.ImproperlyConfigured
    sys.path.append(str(server_location))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphery.settings.test")
    django_setup()

    from backend.models import model_list
    return dict([(model_name, apps.get_model('backend', model_name)) for model_name in model_list])


def get_tutorial_source_path() -> pathlib.Path:
    return pathlib.Path(prompt_session.prompt(message='Please enter the tutorial source folder location: ',
                                              validator=_tutorial_source_folder_validator,
                                              completer=_path_completer))


def gather_tutorial_anchor_info() -> None:
    pass


def get_tutorial_markdown_path(tutorial_source_folder: pathlib.Path) -> pathlib.Path:
    # By convention there should just be one markdown file.
    # but since there is a plugin which can connect markdown snippets
    # maybe I can have a main.md and make the <h1> (#) in the first line
    markdown_files = [file for file in tutorial_source_folder.glob('*.md')]
    return markdown_files[0]


def parse_markdown(text: str) -> str:
    return markdown.markdown(text, extensions=['codehilite', 'md_in_html', 'markdown_del_ins',
                                               'pymdownx.arithmatex', 'pymdownx.details', 'pymdownx.inlinehilite',
                                               'pymdownx.superfences'])
    # TODO add arithmatex required js to the page


def get_new_graph_jsons(resources_location: pathlib.Path) -> list:
    graph_jsons = [file for file in resources_location.glob('*.json') if file.name != 'graph-info.json']
    return graph_jsons


def parse_new_graph_json(graph_jsons: typing.Iterable[pathlib.Path]) -> None:
    pass


def get_entry_module_intel(resources_location: pathlib.Path) -> typing.Tuple:
    return resources_location / 'entry.py', resources_location / 'graph-info.json'


def parse_entry_module() -> None:
    pass


def save_to_local_json() -> None:
    pass
