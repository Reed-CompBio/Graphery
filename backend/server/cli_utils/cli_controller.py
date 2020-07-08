import pathlib
import re
from typing import Tuple, Iterable, List

from django.db.models import QuerySet

from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit import print_formatted_text, prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.document import Document

import markdown

from cli_utils.cli_ui import inline_checkbox_dialog

from .intel_wrapper import *


class CodeSourceFolderValidator(Validator):
    def validate(self, document: Document) -> None:
        code_path = pathlib.Path(document.text)
        entry_py_module = code_path / 'entry.py'
        graph_info = code_path / 'graph-info.json'
        if not code_path.exists() or not entry_py_module.exists() or not graph_info.exists():
            raise ValidationError(message='The code resources folder does not exist or does not contain'
                                          ' an `entry.py` file and a `graph-info.json` file.')


_code_source_folder_validator = CodeSourceFolderValidator()


class TutorialSourceFolderValidator(Validator):
    def validate(self, document: Document) -> None:
        path = pathlib.Path(document.text)
        graph_path = path / 'graphs'
        locale_path = path / 'locale'
        # ehhhhhh
        _code_source_folder_validator.validate(Document(text=(path / 'codes').absolute()))
        if not (path.exists() and graph_path.exists() and locale_path.exists()):
            raise ValidationError(message='The tutorial source file folder structure is not right')


class TutorialAnchorNameValidator(Validator):
    regex = re.compile(r'^[a-zA-Z0-9- ]+\Z')

    def __init__(self):
        super().__init__()
        self.names: List[str] = []

    def __call__(self, tutorials: QuerySet = ()) -> Validator:
        for element in tutorials:
            self.names.append(element.name)
        return self

    def validate(self, document: Document) -> None:
        name = document.text.strip()
        if not self.regex.match(name):
            raise ValidationError(message='The name is not valid. '
                                          'It should only contain letters, numbers, dashes, and spaces.',
                                  cursor_position=len(name) - 1)
        if name in self.names:
            raise ValidationError(message='The name {} is taken. Please enter a new name!'.format(name),
                                  cursor_position=len(name) - 1)


class TutorialAnchorUrlValidator(Validator):
    regex = re.compile(r'^[a-zA-Z0-9-]+\Z')

    def __init__(self):
        super().__init__()
        self.urls: List[str] = []

    def __call__(self, tutorials: QuerySet) -> Validator:
        for element in tutorials:
            self.urls.append(element.url)
        return self

    def validate(self, document: Document) -> None:
        url = document.text.strip()
        if not self.regex.match(url):
            raise ValidationError(message='The url is not valid'
                                          'It should only contain letters, numbers and dashes.',
                                  cursor_position=len(url) - 1)
        if url in self.urls:
            raise ValidationError(message='The url {} is taken. Please enter a new url!'.format(url),
                                  cursor_position=len(url) - 1)


prompt_session = PromptSession[str]()
_path_completer = PathCompleter()
_tutorial_source_folder_validator = TutorialSourceFolderValidator()
_tutorial_anchor_name_validator = TutorialAnchorNameValidator()
_tutorial_anchor_url_validator = TutorialAnchorUrlValidator()


def get_tutorial_source_path() -> pathlib.Path:
    return pathlib.Path(prompt(message='Please enter the tutorial source folder location: ',
                               validator=_tutorial_source_folder_validator,
                               completer=_path_completer))


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


class CommandWrapper:
    @staticmethod
    def gather_tutorial_anchor_info() -> Tuple[str, str, List[CategoryWrapper]]:
        tutorial_query_set = Tutorial.objects.all()

        print_formatted_text('For naming convention, please visit https://poppy-poppy.github.io/Graphery/')
        name: str = prompt(message='Please enter the name of the tutorial: \n',
                           validator=_tutorial_anchor_name_validator(tutorial_query_set)).strip()
        url: str = prompt(message='Please enter the url of the tutorial: \n',
                          validator=_tutorial_anchor_url_validator(tutorial_query_set),
                          default=name.replace(' ', '-')).strip()

        category_query_set = Category.objects.all()
        category_selections = [(element, element.category) for element in category_query_set]

        category_choices: List[CategoryWrapper.model_class] = inline_checkbox_dialog(
            text='Please choose existing categories for this tutorial: ',
            values=category_selections
        ).run()

        if category_choices is None:
            raise KeyboardInterrupt

        new_categories: Iterable[str] = map(
            lambda x: x.strip(),
            prompt('Please enter new categories. Separate with ";"\n').split(';')
        )

        categories = [CategoryWrapper().load_model(category_model)
                      for category_model in category_choices if category_model] + \
                     [CategoryWrapper().set_variables(category_name=category_name)
                      for category_name in new_categories if category_name]

        return url, name, categories

    @classmethod
    def create(cls):
        print(cls.gather_tutorial_anchor_info())

    @classmethod
    def run_command(cls, command: str) -> None:
        getattr(cls, command)()
