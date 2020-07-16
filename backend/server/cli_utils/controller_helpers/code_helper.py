import pathlib
import shutil
from collections import Mapping
from importlib import import_module
from time import time
from typing import Callable

from backend.model.TutorialRelatedModel import Graph

from bundle.GraphObjects.Graph import Graph as CustomGraphObject
from bundle.controller import controller
from bundle.utils.cache_file_helpers import TempSysPathAdder


def code_executor(code_folder: pathlib.Path,
                  graph_object_mappings: Mapping[Graph, CustomGraphObject]) -> Mapping[Graph, Mapping]:
    exec_result = {}

    with controller as folder_creator, \
            folder_creator(f'temp_code_folder_{time()}') as cache_folder, \
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
