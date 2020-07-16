import json
import pathlib
import time
import shutil
from importlib import import_module
from typing import Tuple, List, MutableMapping, Sequence

from bs4 import BeautifulSoup, ResultSet, Tag
from django.db.models import QuerySet

from prompt_toolkit import print_formatted_text

import markdown

from backend.model.UserModel import ROLES

from bundle.controller import controller
from bundle.utils.cache_file_helpers import TempSysPathAdder
from bundle.GraphObjects.Graph import Graph as CustomGraph

from cli_utils.cli_ui import run_interruptable_checkbox_dialog, new_session, \
    info_session
from cli_utils.controller_helpers.cli_validators import name_validator, url_validator, \
    code_source_folder_validator, email_validator, password_validator, username_validator
from .controller_helpers.prompt_consent import proceed_prompt, proceed_publishing_content, \
    proceed_publishing_content_iter
from .controller_helpers.prompt_getters import get_name, get_url, get_location, get_abstract, \
    get_email, get_password
from .controller_helpers.prompt_selectors import select_and_add_categories, select_tutorials, select_authors, \
    select_graph_priority, select_tutorial_lang, select_tutorial, select_graph, select_graph_lang, select_role
from .errors import InvalidGraphJson

from .intel_wrapper import *


def gather_tutorial_anchor_info() -> TutorialAnchorWrapper:
    tutorial_query_set: QuerySet = Tutorial.objects.all()

    print_formatted_text('For naming convention, please visit https://poppy-poppy.github.io/Graphery/')

    name: str = get_name(message='Please enter the name of the tutorial: ',
                         validator=name_validator(tutorial_query_set))

    url: str = get_url(message='Please enter the url of the tutorial: ',
                       validator=url_validator(tutorial_query_set),
                       default=name)

    categories = select_and_add_categories()

    return TutorialAnchorWrapper().set_variables(url=url,
                                                 name=name,
                                                 categories=categories)


def create_tutorial_anchor() -> None:
    anchor_wrapper = gather_tutorial_anchor_info()

    info_session()
    print_formatted_text('Tutorial anchor created')
    print_formatted_text('name: {}'.format(anchor_wrapper.name))
    print_formatted_text('url: {}'.format(anchor_wrapper.url))
    print_formatted_text('categories: {}'.format(anchor_wrapper.categories))

    def actions():
        finalize_prerequisite_wrapper(anchor_wrapper)
        proceed_publishing_content(anchor_wrapper)

    proceed_prompt(actions=actions)


@new_session('Graph Json Location')
def gather_graph_json() -> List[pathlib.Path]:
    graphs: List[pathlib.Path] = []

    graph_location = get_location('Please enter the folder location containing graph jsons: ')
    if graph_location.is_dir():
        graphs.extend(graph_location.glob('*.json'))
    elif graph_location.is_file() and graph_location.suffix == '.json':
        graphs.append(graph_location)

    if len(graphs) < 1:
        raise

    graph_selection_values = [(element, element.name) for element in graphs]

    selected_graph_file_paths = run_interruptable_checkbox_dialog(
        text='Please select the graphs you want to upload',
        values=graph_selection_values,
        default_values=graph_selection_values
    )

    return selected_graph_file_paths


def validate_graph_json(graph_file_path: pathlib.Path) -> Mapping:
    js_string = graph_file_path.read_text()

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


def gather_graph_info(graph_file_path: pathlib.Path) -> GraphWrapper:
    try:
        graph_json_obj: Mapping = validate_graph_json(graph_file_path)
    except InvalidGraphJson:
        raise

    name: str = get_name(message='Please input the name of the graph in {}'.format(graph_file_path.name),
                         validator=name_validator,
                         default=graph_file_path.stem)

    url: str = get_url(message='Please input the url of the graph in {}'.format(graph_file_path.name),
                       validator=url_validator,
                       default=name)

    matching_tutorials = select_tutorials()
    categories: List[CategoryWrapper] = select_and_add_categories()
    authors: List[UserWrapper] = select_authors()

    priority: int = select_graph_priority()

    return GraphWrapper().set_variables(
        url=url,
        name=name,
        categories=categories,
        authors=authors,
        priority=priority,
        cyjs=graph_json_obj,
        tutorials=matching_tutorials
    )


def wrap_graph_jsons(graph_paths: List[pathlib.Path]) -> List[GraphWrapper]:
    return [gather_graph_info(path) for path in graph_paths]


def create_graph() -> None:
    graph_file_paths = gather_graph_json()
    print_formatted_text('The graph json found: ')
    for path in graph_file_paths:
        print_formatted_text('  {}'.format(path.absolute()))

    graph_wrappers: List[GraphWrapper] = wrap_graph_jsons(graph_file_paths)

    info_session()
    print_formatted_text('The following graphs are created: ')
    if graph_wrappers:
        for wrapper in graph_wrappers:
            print_formatted_text(f'{wrapper}')
    else:
        print_formatted_text('None')
        print_formatted_text('No actions taken')
        return

    def actions():
        finalize_prerequisite_wrapper_iter(graph_wrappers)
        proceed_publishing_content_iter(graph_wrappers)

    proceed_prompt(actions=actions)


def get_locale_md_files() -> List[pathlib.Path]:
    source_folder: pathlib.Path = get_location(prompt_text='Please choose the tutorial translation folder')
    md_file_paths: List[pathlib.Path] = [path for path in source_folder.glob('*.md')]

    md_selection_values = [(element, element.name) for element in md_file_paths]

    selected_graph_file_paths = run_interruptable_checkbox_dialog(
        text='Please select the translations you want to upload',
        values=md_selection_values,
        default_values=md_selection_values
    )
    return selected_graph_file_paths


def get_html_soup_from_string(html_string: str) -> BeautifulSoup:
    return BeautifulSoup(html_string, 'html.parser')


def get_img_file(parent_folder: pathlib.Path, img_tag: Tag) -> Optional[pathlib.Path]:
    file_name = img_tag.get('src', None)
    if file_name:
        return parent_folder / file_name
    return None


def move_file_to_static_folder(file: pathlib.Path, static_folder: pathlib.Path, target_folder: pathlib.Path) -> None:
    pass


def process_images(soup: BeautifulSoup, html_parent_folder: pathlib.Path) -> None:
    img_tags: ResultSet = soup.find_all('img')
    for img_tag in img_tags:
        img_file_path = get_img_file(html_parent_folder, img_tag)
        if not img_file_path:
            continue
        # TODO finish this
        # move_file_to_static_folder(img_file_path,)


def parse_markdown(text: str) -> BeautifulSoup:
    result: str = markdown.markdown(text, extensions=['codehilite', 'md_in_html', 'markdown_del_ins',
                                                      'pymdownx.arithmatex', 'pymdownx.details',
                                                      'pymdownx.inlinehilite', 'pymdownx.superfences'])
    soup = get_html_soup_from_string(result)

    return soup
    # TODO add arithmatex required js to the page


def get_meta_info_from_html(soup: BeautifulSoup) -> Tuple[str, str, str]:
    title = soup.h1.text
    soup.h1.decompose()
    content_html = str(soup)
    abstract = str(soup.p)
    return title, content_html, abstract


def gather_locale_md_info(path: pathlib.Path) -> TutorialTranslationContentWrapper:
    try:
        name_and_lang = path.stem.split('.')
        if len(name_and_lang) < 2:
            name, = name_and_lang
            lang = 'en-us'
        elif len(name_and_lang) > 2:
            raise
        else:
            name, lang = name_and_lang
        # TODO I don't think you can do much about it since you can't change the input source in the command line?
        # TODO this is broken because when the lang is not specified, it just returns None
        lang_class: Type[TranslationBase] = select_tutorial_lang(lang)

        content_md = path.read_text()
        soup = parse_markdown(text=content_md)

        md_title, content_html, abstract = get_meta_info_from_html(soup)

        process_images(soup, path.absolute().parent)
        # TODO there is a new line in str(soup)

        title: str = get_name(message='Please edit the title of this tutorial:',
                              default=md_title if md_title else name)

        # TODO again, you can't do much in a command line I guess?
        abstract: str = get_abstract(message='Edit the abstract of this translation:', default=abstract)

        authors = select_authors()
        tutorial_anchor = select_tutorial()

        return TutorialTranslationContentWrapper().set_variables(
            model_class=lang_class,
            title=title,
            authors=authors,
            tutorial_anchor=tutorial_anchor,
            abstract=abstract,
            content_md=content_md,
            content_html=content_html
        )

    except ValueError as e:
        e.args = ('Please follow the naming convention',)


def gather_md_files(md_file_paths: List[pathlib.Path]) -> List[TutorialTranslationContentWrapper]:
    return [gather_locale_md_info(path) for path in md_file_paths]


def create_locale_md() -> None:
    md_paths = get_locale_md_files()
    if not md_paths:
        print_formatted_text('Nothing is selected. Exiting')
        return
    md_file_wrappers = gather_md_files(md_paths)

    # TODO the incorporate edit mode. In the current frame work, this will just load the model from the database
    #  if it's already in there and does basically nothing to it. You should show a warning for now and
    #  and a edit option to it later. Same as for graphs.

    info_session()
    print_formatted_text('The following translations are created: ')
    for wrapper in md_file_wrappers:
        print_formatted_text(f'{wrapper}')

    def actions():
        finalize_prerequisite_wrapper_iter(md_file_wrappers)

        proceed_publishing_content_iter(md_file_wrappers)

    proceed_prompt(actions=actions)


def get_code_source_folder() -> pathlib.Path:
    return get_location(validator=code_source_folder_validator)


def get_code_text_and_graph_req(source_folder_path: pathlib.Path) -> Tuple[str, Sequence[str]]:
    json_obj = json.loads((source_folder_path / 'graph-info.json').read_text())

    if 'required_graphs' in json_obj:
        return (source_folder_path / 'entry.py').read_text(), json_obj['required_graphs']
    raise


def code_executor(code_folder: pathlib.Path,
                  graph_object_mappings: Mapping[Graph, CustomGraph]) -> Mapping[Graph, Mapping]:
    exec_result = {}

    with controller as folder_creator, \
            folder_creator(f'temp_code_folder_{time.time()}') as cache_folder, \
            TempSysPathAdder(cache_folder):
        for any_file in code_folder.glob('*.*'):
            if any_file.is_file():
                # noinspection PyTypeChecker
                shutil.copy(any_file, cache_folder.cache_folder_path / any_file.name)

        try:
            imported_module = import_module('entry')

            # TODO a better name maybe?
            if not hasattr(imported_module, 'graph_object'):
                raise ValueError('The `graph_object` is not used, which violates the naming convention')

            main_function = getattr(imported_module, 'main', None)

            if not main_function or not isinstance(main_function, Callable):
                raise ValueError('There is not main function or it is not valid')

            for graph_name, graph_obj in graph_object_mappings.items():
                # I did not see this coming. I need to change the controller
                controller.purge_records()

                setattr(imported_module, 'graph_object', graph_obj)
                main_function()

                controller.generate_processed_record()

                exec_result[graph_name] = controller.get_processed_result()
        except ImportError as e:
            e.args = (f'Cannot import `entry` moduel. Error: {e}', )
            raise
        except Exception as e:
            e.args = (f'Unknown exception occurs in executing the code. Error: {e}',)
            raise

        return exec_result


def gather_code_info(code_folder: pathlib.Path) -> Tuple[CodeWrapper, Sequence[ExecResultJsonWrapper]]:
    code_text, required_graph_urls = get_code_text_and_graph_req(code_folder)
    if len(required_graph_urls) < 1:
        raise ValueError('The graph-info.json must contain at least one graph url')

    tutorial_anchor = select_tutorial()

    graph_id_obj_mapping: MutableMapping[Graph, CustomGraph] = {}

    # TODO maybe change this part. Not using url may be a better idea
    for graph_url in required_graph_urls:
        graph_model_obj: Graph = Graph.objects.get(url=graph_url)
        graph_obj: CustomGraph = CustomGraph.graph_generator(graph_model_obj.cyjs)
        graph_id_obj_mapping[graph_model_obj] = graph_obj

    exec_result_mapping: Mapping[Graph, Mapping] = code_executor(code_folder, graph_id_obj_mapping)

    code_wrapper: CodeWrapper = CodeWrapper().set_variables(
        tutorial=tutorial_anchor,
        code=code_text
    )
    # TODO something's wrong here. The code is not in the database

    exec_result_wrappers = [ExecResultJsonWrapper().set_variables(
        code=code_wrapper,
        graph=GraphWrapper().load_model(graph_obj),
        json=exec_result_json_obj
    ) for graph_obj, exec_result_json_obj in exec_result_mapping.items()]

    return code_wrapper, exec_result_wrappers


def create_code_obj() -> None:
    code_source_folder = get_code_source_folder()
    code_wrapper, exec_result_wrappers = gather_code_info(code_source_folder)

    info_session()
    print_formatted_text('Code: {}'.format(code_wrapper))
    print_formatted_text('Execution results: ')
    for wrapper in exec_result_wrappers:
        print_formatted_text(f'{wrapper}')

    def actions():
        finalize_prerequisite_wrapper(code_wrapper)
        finalize_prerequisite_wrapper_iter(exec_result_wrappers)

    proceed_prompt(actions=actions)


def get_graph_locale_info_md(parent_folder: pathlib.Path) -> List[pathlib.Path]:
    graph_locale_file_values = [(file, file.name) for file in parent_folder.glob('*.md')]

    graph_locale_files: List[pathlib.Path] = run_interruptable_checkbox_dialog(
        text="Please select the graphs' info you want to upload",
        values=graph_locale_file_values,
        default_values=graph_locale_file_values
    )

    return graph_locale_files


def gather_graph_locale_info(info_files: List[pathlib.Path]) -> List[GraphTranslationContentWrapper]:
    locale_infos: List[GraphTranslationContentWrapper] = []
    for info_file in info_files:
        try:
            file_name, lang = info_file.name.split('.')

            language_model: Type[GraphTranslationBase] = select_graph_lang(lang)

            md_title, abstract, _ = parse_markdown(info_file.read_text())

            title = get_name(message='Please input the title of this graph',
                             default=md_title if md_title else file_name)

            abstract: str = get_abstract(message='Edit the abstract of this translation', default=abstract)

            graph_anchor: Graph = select_graph()

            locale_infos.append(GraphTranslationContentWrapper().set_variables(
                model_class=language_model,
                title=title,
                abstract=abstract,
                graph_anchor=graph_anchor
            ))
        except ValueError:
            raise
        except TypeError:
            raise

    return locale_infos


def create_graph_content_trans() -> None:
    graph_info_location: pathlib.Path = get_location()
    graph_info_md_files: List[pathlib.Path] = get_graph_locale_info_md(graph_info_location)
    if len(graph_info_md_files) < 1:
        print_formatted_text('None is selected. Exited.')
    graph_content_wrappers: List[GraphTranslationContentWrapper] = gather_graph_locale_info(graph_info_md_files)

    def actions():
        finalize_prerequisite_wrapper_iter(graph_content_wrappers)

        proceed_publishing_content_iter(graph_content_wrappers)

    info_session()
    print_formatted_text('Graph info translations: ')
    for wrapper in graph_content_wrappers:
        print_formatted_text(f'{wrapper}')

    proceed_prompt(actions=actions)


def enter_password() -> Optional[str]:
    password = get_password(message='Please enter the password: ', validator=password_validator)
    reenter_password = get_password(message='Please reenter the password: ', validator=password_validator)
    if password == reenter_password:
        return reenter_password
    return None


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
