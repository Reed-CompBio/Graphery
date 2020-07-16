import json
import pathlib
from typing import List, Mapping

from prompt_toolkit import print_formatted_text

from cli_utils.cli_ui import new_session, run_interruptable_checkbox_dialog

from cli_utils.command_helpers.command_base import CommandBaseOverIterable

from cli_utils.controller_helpers.cli_validators import name_validator, url_validator
from cli_utils.controller_helpers.prompt_consent import proceed_publishing_content_iter
from cli_utils.controller_helpers.prompt_getters import get_name, get_url, get_location
from cli_utils.controller_helpers.prompt_selectors import select_tutorials, select_and_add_categories, select_authors, \
    select_graph_priority

from cli_utils.errors import InvalidGraphJson

from cli_utils.intel_wrappers.intel_wrapper import GraphWrapper, finalize_prerequisite_wrapper_iter


class GraphCreator(CommandBaseOverIterable):
    def __init__(self):
        super().__init__('Create Graph')
        self.graph_wrappers = []

    def output_created_confirmation_info(self) -> None:
        print_formatted_text('The following graphs are created: ')
        for wrapper in self.graph_wrappers:
            print_formatted_text(f'{wrapper}')

    def output_not_created_confirmation_info(self) -> None:
        print_formatted_text('No graphs are created')
        print_formatted_text('None')
        print_formatted_text('No actions taken')

    @new_session('Graph Json Location')
    def gather_graph_json(self) -> List[pathlib.Path]:
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

    @staticmethod
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

    def gather_graph_info(self, graph_file_path: pathlib.Path):
        try:
            self.set_attr('cyjs', GraphCreator.validate_graph_json(graph_file_path))
        except InvalidGraphJson:
            raise

        self.new_attr()

        name = self.set_attr('name',
                             get_name(message='Please input the name of the graph in {}'.format(graph_file_path.name),
                                      validator=name_validator,
                                      default=graph_file_path.stem))

        self.set_attr('url', get_url(message='Please input the url of the graph in {}'.format(graph_file_path.name),
                                     validator=url_validator,
                                     default=name))

        self.set_attr('tutorials', select_tutorials())
        self.set_attr('categories', select_and_add_categories())
        self.set_attr('authors', select_authors())

        self.set_attr('priority', select_graph_priority())

    def gather_info(self) -> None:
        graph_file_paths = self.gather_graph_json()
        print_formatted_text('The graph json found: ')
        for path in graph_file_paths:
            print_formatted_text('  {}'.format(path.absolute()))

        # TODO not dry enough
        for path in graph_file_paths:
            try:
                self.gather_graph_info(path)
            except Exception as e:
                deleted_ele = self.del_attr()
                e.args = (f'Exception occurs when creating a graph {deleted_ele}. Error: {e}', )
                # TODO
                raise

    def create(self):
        self.graph_wrappers.extend(GraphWrapper().set_variables(**info_dict) for info_dict in self.command_attrs)

        return not not self.graph_wrappers

    def proceed_helper(self):
        finalize_prerequisite_wrapper_iter(self.graph_wrappers)
        proceed_publishing_content_iter(self.graph_wrappers)
