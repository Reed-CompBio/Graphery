#!/usr/bin/env python3
import pathlib
import sys
import json
from importlib import import_module
from typing import Union, Mapping, Callable, List
from wsgiref.simple_server import make_server
from multiprocessing import Pool, TimeoutError

from bundle.GraphObjects.Graph import Graph
from bundle.utils.cache_file_helpers import TempSysPathAdder, get_md5_of_a_string
from bundle.controller import controller
from server_utils.params import TIMEOUT_SECONDS, REQUEST_CODE_NAME, ONLY_ACCEPTED_ORIGIN, ACCEPTED_ORIGIN, \
    REQUEST_GRAPH_NAME, GRAPH_OBJ_ANCHOR_NAME, ENTRY_PY_MODULE_NAME, MAIN_FUNCTION_NAME, ENTRY_PY_FILE_NAME
from server_utils.utils import arg_parser, valid_version, create_error_response, create_data_response


class ExecutionException(Exception):
    pass


def main(port: int):
    with make_server('127.0.0.1', port, application) as httpd:
        print('Press <ctrl+c> to stop the server. ')
        print(f'Ready for Python code on port {port} ...')
        httpd.serve_forever()


def execute(code: str, graph_json: Union[str, Mapping], auto_delete_cache: bool = False) -> List[Mapping]:
    folder_hash = get_md5_of_a_string(code)

    try:
        graph_json_obj = json.loads(graph_json) if isinstance(graph_json, str) else graph_json

        graph_object = Graph.graph_generator(graph_json_obj)
    except Exception as e:
        raise ExecutionException(f'Cannot import graph objects. Error: {e}')

    with controller as folder_creator, \
            folder_creator(folder_hash, auto_delete=auto_delete_cache) as cache_folder, \
            TempSysPathAdder(cache_folder):
        try:
            entry_file: pathlib.Path = cache_folder / ENTRY_PY_FILE_NAME

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
                raise ValueError('There is not main function or it is not valid')

            if not hasattr(imported_module, GRAPH_OBJ_ANCHOR_NAME):
                raise ValueError('There is not graph object, which violates the naming convention')

            setattr(imported_module, GRAPH_OBJ_ANCHOR_NAME, graph_object)

            controller.purge_records()
            main_function()
            controller.generate_processed_record()
        except Exception as e:
            raise ExecutionException(e)
        finally:
            del sys.modules[ENTRY_PY_MODULE_NAME]
            del imported_module

    return controller.get_processed_result()


def time_out_execute(*args, **kwargs):
    with Pool(processes=1) as pool:
        try:
            result = pool.apply_async(func=execute, args=args, kwds=kwargs)

            response_dict = create_data_response({'exec_result': result.get(timeout=TIMEOUT_SECONDS)})
        except TimeoutError:
            response_dict = create_error_response(f'Timeout: Code running timed out after {TIMEOUT_SECONDS} s.')
        except ExecutionException as e:
            response_dict = create_error_response(f'Exception: {e}.')
        except Exception as e:
            response_dict = create_error_response(f'Unknown Exception: {e}.')

        print('Execution done.')
    return response_dict


def application(environ: Mapping, start_response: Callable):
    response_code = '200 OK'
    headers = [('Content-Type', 'application/json')]

    # origin check
    origin = environ.get('HTTP_ORIGIN', '')
    if ONLY_ACCEPTED_ORIGIN and origin.find(ACCEPTED_ORIGIN) == -1:
        content = create_error_response(f'The ORIGIN, {ACCEPTED_ORIGIN}, is not accepted.')
    else:
        try:
            content = application_helper(environ)
        except Exception as e:
            content = create_error_response(f'An exception occurs in the server. Error: {e}')

    headers.append(('Access-Control-Allow-Origin', origin))
    start_response(response_code, headers)
    return [json.dumps(content).encode()]


def application_helper(environ):
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')

    # info page
    if method == 'GET' and path == '/env':
        return create_data_response(environ)

    # entry point check
    if method != 'POST' or path != '/run':
        # TODO change the response string
        return create_error_response('Bad Request: Wrong Methods.')

    # get request content
    request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    request_json_object = json.loads(request_body)

    if REQUEST_CODE_NAME not in request_json_object:
        return create_error_response('No Code Snippets Embedded In The Request.')

    if REQUEST_GRAPH_NAME not in request_json_object:
        return create_error_response('No Graph Intel Embedded In The Request.')

    # execute program with timed out
    return time_out_execute(code=request_json_object[REQUEST_CODE_NAME],
                                   graph_json=request_json_object[REQUEST_GRAPH_NAME])


if __name__ == '__main__':
    if not valid_version():
        exit(1)

    try:
        main(arg_parser()['port'])
    except KeyboardInterrupt:
        print('Interrupted by keyboard.')
    except Exception as exc:
        print(f'Unknown exception occurred. Error: {exc}')
    finally:
        print('Stopped the server.')
