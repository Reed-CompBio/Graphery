import json
import pathlib
import re
from typing import Tuple, List, Union, Generator

from django.db.models import QuerySet
from django.db.transaction import commit, rollback

from prompt_toolkit.completion import PathCompleter
from prompt_toolkit import print_formatted_text, prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.document import Document

import markdown

from cli_utils.cli_ui import interruptable_checkbox_dialog, new_session, inline_radio_dialog
from .errors import InvalidGraphJson

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


class NameValidator(Validator):
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


class UrlValidator(Validator):
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


class LocationValidator(Validator):
    def validate(self, document: Document) -> None:
        if not pathlib.Path(document.text).exists():
            raise ValidationError(message='Please input a valid path!')


_path_completer = PathCompleter()
_tutorial_source_folder_validator = TutorialSourceFolderValidator()
_name_validator = NameValidator()
_url_validator = UrlValidator()
_location_validator = LocationValidator()


def new_line_prompt(*args, **kwargs) -> str:
    message = kwargs.pop('message', '\n') + '\n'
    return prompt(message=message, *args, **kwargs)


def get_tutorial_source_path() -> pathlib.Path:
    return pathlib.Path(new_line_prompt(message='Please enter the tutorial source folder location: ',
                                        validator=_tutorial_source_folder_validator,
                                        completer=_path_completer))


def get_location(prompt_text: str = 'Please enter location') -> pathlib.Path:
    return pathlib.Path(new_line_prompt(prompt_text,
                                        validator=_location_validator,
                                        completer=_path_completer, ))


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


@new_session('select and add categories')
def select_and_add_categories() -> List[CategoryWrapper]:
    category_query_set: QuerySet = Category.objects.all()
    category_selections: List[Tuple[Category, str]] = [(model, model.category) for model in category_query_set]

    category_choices: List[Category] = interruptable_checkbox_dialog(
        text='Please choose existing categories: ',
        values=category_selections
    )

    new_categories: Iterable[str] = map(
        lambda x: x.strip(),
        new_line_prompt('Please enter new categories. Separate with ";"').split(';')
    )

    return [CategoryWrapper().load_model(category_model)
            for category_model in category_choices if category_model] + \
           [CategoryWrapper().set_variables(category_name=category_name)
            for category_name in new_categories if category_name]


@new_session('select authors')
def select_authors() -> List[UserWrapper]:
    user_query_set: QuerySet = User.objects.all()
    user_selections: List[Tuple[User, str]] = [(model, f'{model.username}: {model.email}') for model in user_query_set]

    user_choices: List[User] = interruptable_checkbox_dialog(
        text='Please choose authors: ',
        values=user_selections
    )

    return [UserWrapper().load_model(user_model) for user_model in user_choices if user_model]


@new_session('select graph priority')
def select_graph_priority() -> int:
    return int(inline_radio_dialog(text='Please select the priority of this graph',
                                   values=[(60, 'major graph',),
                                           (40, 'minor graph',),
                                           (20, 'trivial graph')]).run())


@new_session('select matching tutorials')
def select_tutorials() -> List[TutorialAnchorWrapper]:
    tutorial_query_set = Tutorial.objects.all()
    tutorial_selections = [(model, f'{model.url}: {model.name}') for model in tutorial_query_set]

    tutorial_choices: List[Tutorial] = interruptable_checkbox_dialog(
        text='Please select tutorials',
        values=tutorial_selections
    )

    return [TutorialAnchorWrapper().load_model(tutorial_model) for tutorial_model in tutorial_choices if tutorial_model]


def gather_tutorial_anchor_info() -> Tuple[str, str, List[CategoryWrapper]]:
    tutorial_query_set: QuerySet = Tutorial.objects.all()

    print_formatted_text('For naming convention, please visit https://poppy-poppy.github.io/Graphery/')

    name: str = get_name(message='Please enter the name of the tutorial: ',
                         validator=_name_validator(tutorial_query_set))

    url: str = get_url(message='Please enter the url of the tutorial: \n',
                       validator=_url_validator(tutorial_query_set),
                       default=name)

    categories = select_and_add_categories()

    return url, name, categories


def wrap_tutorial_anchor(tutorial_anchor_info: Tuple[str, str, List[CategoryWrapper]]) -> TutorialAnchorWrapper:
    tutorial_anchor_wrapper = TutorialAnchorWrapper().set_variables(url=tutorial_anchor_info[0],
                                                                    name=tutorial_anchor_info[1],
                                                                    categories=tutorial_anchor_info[2])
    return tutorial_anchor_wrapper


def create_tutorial_anchor() -> None:
    anchor_wrapper = wrap_tutorial_anchor(gather_tutorial_anchor_info())
    print_formatted_text('Tutorial anchor created')
    print_formatted_text('name: {}'.format(anchor_wrapper.name))
    print_formatted_text('url: {}'.format(anchor_wrapper.url))
    print_formatted_text('categories: {}'.format(anchor_wrapper.categories))
    result = prompt('Proceed: y/N: ')

    if result.lower() == 'Y':
        anchor_wrapper.prepare_model()
        anchor_wrapper.finalize_model()
        commit()
        print_formatted_text('Changes committed')
    else:
        print_formatted_text('Changes not saved. Rolling back.')
        rollback()
        print_formatted_text('Rolled back.')


@new_session('Graph Json Location')
def gather_graph_json() -> List[pathlib.Path]:
    graphs: List[pathlib.Path] = []

    graph_location = get_location('Please enter find your graphs: \n')
    if graph_location.is_dir():
        graphs.extend(graph_location.glob('*.json'))
    elif graph_location.is_file() and graph_location.suffix == '.json':
        graphs.append(graph_location)

    if len(graphs) < 1:
        raise

    return graphs


def validate_graph_json(graph_file_path: pathlib.Path) -> Mapping:
    with graph_file_path.open(mode='r') as file:
        js_string = file.read()

    try:
        js_obj = json.loads(js_string)
        if js_obj.get('elements', None) is None:
            raise InvalidGraphJson('The graph json (cyjs) must contain `element` object')
    except TypeError as e:
        raise InvalidGraphJson('The json input is not right: {}'.format(e))
    except json.JSONDecodeError:
        raise InvalidGraphJson("The json is malformatted. If you believe it's the program's fault, "
                               "please contact the developer")

    # TODO load the json into the custom graph object

    return js_obj


def gather_graph_info(graph_file_paths: List[pathlib.Path]) -> Generator[GraphWrapper]:
    for graph_file_path in graph_file_paths:
        try:
            graph_json_obj: Mapping = validate_graph_json(graph_file_path)
        except InvalidGraphJson:
            raise

        name: str = get_name(message='Please input the name of the graph in {}'.format(graph_file_path.name),
                             validator=_name_validator,
                             default=graph_file_path.stem)

        url: str = get_url(message='Please input the url of the graph in {}'.format(graph_file_path.name),
                           validator=_url_validator,
                           default=name)

        matching_tutorials = select_tutorials()
        categories: List[CategoryWrapper] = select_and_add_categories()
        authors: List[UserWrapper] = select_authors()

        priority: int = select_graph_priority()

        yield GraphWrapper().set_variables(
            url=url,
            name=name,
            categories=categories,
            authors=authors,
            priority=priority,
            cyjs=graph_json_obj,
            tutorials=matching_tutorials
        )


def wrap_graph_jsons(graph_paths: List[pathlib.Path]) -> List[GraphWrapper]:
    wrappers = []
    for wrapper in gather_graph_info(graph_paths):
        wrappers.append(wrapper)

    return wrappers


def create_graph() -> None:
    graph_file_paths = gather_graph_json()
    print_formatted_text('The graph json found: ')
    for path in graph_file_paths:
        print_formatted_text('  {}'.format(path.absolute()))

    graph_selection_values = [(element, element.name) for element in graph_file_paths]

    selected_graph_file_paths = interruptable_checkbox_dialog(
        text='Please select the graphs you want to upload',
        values=graph_selection_values,
        default_values=graph_selection_values
    )
    graph_wrappers: List[GraphWrapper] = wrap_graph_jsons(selected_graph_file_paths)

    print_formatted_text('The following graphs are created: ')
    for wrapper in graph_wrappers:
        print_formatted_text(f'{wrapper}')

    proceed = prompt('Proceed: (y/N)')
    if proceed.lower() == 'y':
        for wrapper in graph_wrappers:
            wrapper.prepare_model()
            wrapper.finalize_model()
        commit()
        print_formatted_text('Changes committed.')
    else:
        print_formatted_text('Changes not saved. Rolling back.')
        rollback()
        print_formatted_text('Rolled back')


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


def get_entry_module_intel(resources_location: pathlib.Path) -> Tuple:
    return resources_location / 'entry.py', resources_location / 'graph-info.json'


def parse_entry_module() -> None:
    pass


def save_to_local_json() -> None:
    pass


class CommandWrapper:
    # use instance instead of class, so that I can have a recent create list.
    @staticmethod
    def create():
        create_tutorial_anchor()

    @staticmethod
    def add():
        print_formatted_text('Coming soon!')

    @staticmethod
    def modify():
        print_formatted_text('Coming soon!')

    @classmethod
    def run_command(cls, command: str) -> None:
        getattr(cls, command)()
