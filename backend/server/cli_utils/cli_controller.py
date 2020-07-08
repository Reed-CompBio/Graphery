import os
import pathlib
import sys
from typing import Mapping, Callable, Tuple, Iterable, List

from django.apps import apps
from django import setup as django_setup
from django.db import models


import markdown


def get_server_location() -> pathlib.Path:
    # return pathlib.Path(
    #     prompt_session.prompt(message='Please reenter the Django server location which contains `manage.py` '
    #                                   'file: ',
    #                           validator=_server_path_validator,
    #                           completer=_path_completer
    #                           ))
    pass


def init_server_settings(server_location: pathlib.Path) -> Mapping[str, models.Model]:
    # TODO this will raise exceptions
    #  django.core.exceptions.ImproperlyConfigured
    sys.path.append(str(server_location))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphery.settings.test")
    django_setup()

    from backend.models import model_list
    return dict([(model_name, apps.get_model('backend', model_name)) for model_name in model_list])


def get_tutorial_source_path() -> pathlib.Path:
    # return pathlib.Path(prompt_session.prompt(message='Please enter the tutorial source folder location: ',
    #                                           validator=_tutorial_source_folder_validator,
    #                                           completer=_path_completer))
    pass


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


def parse_new_graph_json(graph_jsons: Iterable[pathlib.Path]) -> None:
    pass


def get_entry_module_intel(resources_location: pathlib.Path) -> Tuple:
    return resources_location / 'entry.py', resources_location / 'graph-info.json'


def parse_entry_module() -> None:
    pass


def save_to_local_json() -> None:
    pass


class Starter:
    def __init__(self):
        self.splash_screen_choices: List[Tuple[str, Callable]] = [
            ('Cancel', lambda: None)
        ]
