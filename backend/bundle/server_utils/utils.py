import argparse
import json
import sys
import pathlib
from importlib import import_module
from typing import Mapping, Any, Callable, Union, List, Tuple

from .params import DEFAULT_PORT, GRAPH_OBJ_ANCHOR_NAME, ENTRY_PY_MODULE_NAME, MAIN_FUNCTION_NAME, \
    ENTRY_PY_FILE_NAME

from ..GraphObjects.Graph import Graph
from ..utils.cache_file_helpers import TempSysPathAdder, get_md5_of_a_string
from ..controller import controller


class ExecutionException(Exception):
    pass


def arg_parser() -> Mapping[str, int]:
    parser = argparse.ArgumentParser(description='Graphery Local Server')
    parser.add_argument('-p', '--port',
                        default=DEFAULT_PORT,
                        type=int,
                        help='The port the local server will run on')

    args: argparse.Namespace = parser.parse_args()
    return vars(args)


def create_error_response(message: str) -> dict:
    return {
        'errors': [{
            'message': message
        }]
    }


def create_data_response(data: Any) -> dict:
    return {
        'data': data if isinstance(data, Mapping) else {'info': data}
    }


def execute(code: str, graph_json: Union[str, Mapping], auto_delete_cache: bool = False) -> Tuple[str, List[Mapping]]:
    folder_hash: str = get_md5_of_a_string(code)

    try:
        graph_json_obj = json.loads(graph_json) if isinstance(graph_json, str) else graph_json

        graph_object = Graph.graph_generator(graph_json_obj)
    except Exception as e:
        raise ExecutionException(f'Cannot import graph objects. Error: {e}')

    with controller as folder_creator, \
            folder_creator(folder_hash, auto_delete=auto_delete_cache) as cache_folder, \
            TempSysPathAdder(cache_folder):
        try:
            entry_file: pathlib.Path = cache_folder.cache_folder_path / ENTRY_PY_FILE_NAME

            entry_file.write_text(code)
        except Exception as e:
            raise ExecutionException(f'Cannot create temporary execution file. Error: {e}')

        try:
            imported_module = import_module(ENTRY_PY_MODULE_NAME)

        except Exception as e:
            raise ExecutionException(f'Cannot import module. Error: {e}')

        try:
            main_function = getattr(imported_module, MAIN_FUNCTION_NAME, None)

            if not main_function or not isinstance(main_function, Callable):
                raise ExecutionException('There is no main function or it is not valid')

            if not hasattr(imported_module, GRAPH_OBJ_ANCHOR_NAME):
                raise ExecutionException('There is no graph object, which violates the naming convention')

            setattr(imported_module, GRAPH_OBJ_ANCHOR_NAME, graph_object)

            controller.purge_records()
            main_function()
            controller.generate_processed_record()
        except Exception as e:
            raise ExecutionException(e)
        finally:
            del sys.modules[ENTRY_PY_MODULE_NAME]
            del imported_module

    return folder_hash, controller.get_processed_result()
