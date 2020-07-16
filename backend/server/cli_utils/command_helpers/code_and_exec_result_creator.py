import pathlib
from typing import MutableMapping, Mapping, Optional, List

from prompt_toolkit import print_formatted_text

from backend.model.TutorialRelatedModel import Graph

from cli_utils.command_helpers.command_base import CommandBaseOverIterable

from cli_utils.controller_helpers.code_helper import code_executor
from cli_utils.controller_helpers.prompt_getters import get_code_text_and_graph_req, get_code_source_folder
from cli_utils.controller_helpers.prompt_selectors import select_tutorial

from cli_utils.intel_wrappers.intel_wrapper import CodeWrapper, ExecResultJsonWrapper, GraphWrapper, \
    finalize_prerequisite_wrapper, finalize_prerequisite_wrapper_iter, TutorialAnchorWrapper

from bundle.GraphObjects.Graph import Graph as CustomGraphObject


class CodeExecCreator(CommandBaseOverIterable):
    def __init__(self):
        super(CodeExecCreator, self).__init__('Create/Overwrite Code and Execution Result')
        self.code_wrapper: Optional[CodeWrapper] = None
        self.exec_result_wrappers: List[ExecResultJsonWrapper] = []

    def gather_info(self) -> None:
        code_source_folder: pathlib.Path = get_code_source_folder()
        code_text, required_graph_urls = get_code_text_and_graph_req(code_source_folder)
        if len(required_graph_urls) < 1 or not code_text:
            raise ValueError('The graph-info.json must contain at least one graph url')

        tutorial_anchor: TutorialAnchorWrapper = select_tutorial()

        graph_id_obj_mapping: MutableMapping[Graph, CustomGraphObject] = {}

        # TODO maybe change this part. Not using url may be a better idea
        for graph_url in required_graph_urls:
            graph_model_obj: Graph = Graph.objects.get(url=graph_url)
            graph_obj: CustomGraphObject = CustomGraphObject.graph_generator(graph_model_obj.cyjs)
            graph_id_obj_mapping[graph_model_obj] = graph_obj

        exec_result_mapping: Mapping[Graph, Mapping] = code_executor(code_source_folder, graph_id_obj_mapping)

        # TODO something's wrong here. The code is not in the database
        self.code_wrapper = CodeWrapper().set_variables(
            tutorial=tutorial_anchor,
            code=code_text
        )

        self.exec_result_wrappers = [ExecResultJsonWrapper().set_variables(
            code=self.code_wrapper,
            graph=GraphWrapper().load_model(graph_obj),
            json=exec_result_json_obj
        ) for graph_obj, exec_result_json_obj in exec_result_mapping.items()]

    def output_created_confirmation_info(self) -> None:
        print_formatted_text('Code: {}'.format(self.code_wrapper))
        print_formatted_text('Execution results: ')
        for wrapper in self.exec_result_wrappers:
            print_formatted_text(f'{wrapper}')

    def output_not_created_confirmation_info(self) -> None:
        print_formatted_text('No code is executed')

    def create(self) -> bool:
        # TODO change this
        return True

    def proceed_helper(self) -> None:
        finalize_prerequisite_wrapper(self.code_wrapper)
        finalize_prerequisite_wrapper_iter(self.exec_result_wrappers)
