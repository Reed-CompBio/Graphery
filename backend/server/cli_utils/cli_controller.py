import json
import pathlib
import time
import shutil
from importlib import import_module
from typing import Tuple, List, MutableMapping, Sequence

from bs4 import BeautifulSoup, ResultSet, Tag

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
from .controller_helpers.content_creator_helper import get_file_name_and_lang
from .controller_helpers.prompt_consent import proceed_prompt, proceed_publishing_content_iter
from .controller_helpers.prompt_getters import get_name, get_url, get_location, get_abstract, \
from .controller_helpers.prompt_selectors import select_and_add_categories, select_tutorials, select_authors, \
    select_graph_priority, select_tutorial_lang, select_tutorial, select_graph, select_graph_lang, select_role
from .errors import InvalidGraphJson

from .intel_wrapper import *


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
            file_name, lang = get_file_name_and_lang(info_file.stem)

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
