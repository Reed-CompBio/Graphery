#!/usr/bin/env python3
import argparse
import pathlib
import sys
import json
from importlib import import_module
from typing import Union, Mapping, Callable, List, Optional
from wsgiref.simple_server import make_server
from multiprocessing import Pool, TimeoutError

from bundle.GraphObjects.Graph import Graph
from bundle.utils.cache_file_helpers import TempSysPathAdder, get_md5_of_a_string
from bundle.controller import controller


def valid_version():
    v = sys.version_info
    if v.major == 3 and v.minor >= 8:
        return True
    print('Your current python is %d.%d. Please use Python 3.8.' % (v.major, v.minor))
    return False


if not valid_version():
    exit(1)


class ExecutionException(Exception):
    pass


DEFAULT_PORT: int = 7590
ONLY_ACCEPTED_ORIGIN: bool = False
ACCEPTED_ORIGIN: str = ''
TIMEOUT_SECONDS: int = 10

ENTRY_PY_MODULE_NAME: str = 'entry'
ENTRY_PY_FILE_NAME: str = f'{ENTRY_PY_MODULE_NAME}.py'
MAIN_FUNCTION_NAME: str = 'main'
GRAPH_OBJ_ANCHOR_NAME: str = 'graph_object'

REQUEST_CODE_NAME: str = 'code'
REQUEST_GRAPH_NAME: str = 'graph'


def arg_parser() -> Mapping[str, int]:
    parser = argparse.ArgumentParser(description='Graphery Local Server')
    parser.add_argument('-p', '--port',
                        default=DEFAULT_PORT,
                        type=int,
                        help='The port the local server will run on')

    args: argparse.Namespace = parser.parse_args()
    return vars(args)


def main(port: int):
    httpd = make_server('127.0.0.1', port, application)
    print('Press <ctrl+c> to stop the server. ')
    print(f'Ready for Python code on port {port} ...')
    httpd.serve_forever()


def store_exec_cache(cache_folder: pathlib.Path, graph_hash: str, exec_result: List) -> None:
    cache_file: pathlib.Path = cache_folder / 'exec_cache.json'
    if cache_file.exists():
        json_obj = json.loads(cache_file.read_text())
    else:
        json_obj = {}

    json_obj[graph_hash] = exec_result
    cache_file.write_text(json.dumps(json_obj))


def get_exec_cache(cache_folder: pathlib.Path, graph_hash: str) -> Optional[List]:
    cache_file: pathlib.Path = cache_folder / 'exec_cache.json'
    if not cache_file.exists():
        return None

    json_obj: Mapping = json.loads(cache_file.read_text())

    return json_obj.get(graph_hash, None)


def execute(code: str, graph_json: Union[str, Mapping], auto_delete_cache: bool = False) -> List[Mapping]:
    folder_hash = get_md5_of_a_string(code)
    graph_hash = get_md5_of_a_string(graph_json)

    graph_json_obj = json.loads(graph_json) if isinstance(graph_json, str) else graph_json

    graph_object = Graph.graph_generator(graph_json_obj)

    with controller as folder_creator, \
            folder_creator(folder_hash, auto_delete=auto_delete_cache) as cache_folder, \
            TempSysPathAdder(cache_folder):
        entry_file: pathlib.Path = cache_folder / ENTRY_PY_FILE_NAME

        if not entry_file.exists():
            entry_file.touch()
            entry_file.write_text(code)
        else:
            cache_result = get_exec_cache(cache_folder=cache_folder, graph_hash=graph_hash)
            if cache_result:
                return cache_result

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

    exec_result = controller.get_processed_result()
    if not auto_delete_cache:
        store_exec_cache(cache_folder, graph_hash, exec_result)

    return controller.get_processed_result()


def time_out_execute(*args, **kwargs):
    response_dict = {}
    with Pool(processes=1) as pool:
        result = pool.apply_async(func=execute, args=args, kwds=kwargs)
        try:
            response_dict['data'] = result.get(timeout=TIMEOUT_SECONDS)
        except TimeoutError:
            response_dict['errors'] = dict(type='Timeout', message=f'Code running timed out after {TIMEOUT_SECONDS} s.')
        except ExecutionException as e:
            response_dict['errors'] = dict(type='Exception', message=str(e))
        except Exception as e:
            response_dict['errors'] = dict(type='Unknown Exception', message=str(e))

        print('Execution done.')
    return response_dict


def application(environ, start_response):
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')

    # info page
    if method == 'GET' and path == '/env':
        start_response('200 OK', [('Content-Type', 'text/html')])
        rep = [b'<html><head><title>ENV</title></head><body>']
        for k, v in environ.items():
            p = '<p>%s = %s' % (k, str(v))
            rep.append(p.encode('utf-8'))
        rep.append(b'</html>')
        return rep

    # entry point check
    if method != 'POST' or path != '/run':
        start_response('400 Bad Request', [('Content-Type', 'application/json')])
        return [b'{"error":"bad_request","res":"wrong_method"}']

    # origin check
    headers = [('Content-Type', 'application/json')]
    origin = environ.get('HTTP_ORIGIN', '')
    if ONLY_ACCEPTED_ORIGIN and origin.find(ACCEPTED_ORIGIN) == -1:
        start_response('400 Bad Request', [('Content-Type', 'application/json')])
        return [b'{"error":"invalid_origin"}']

    # get request content
    request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    request_json_object = json.loads(request_body)
    if REQUEST_CODE_NAME not in request_json_object or REQUEST_GRAPH_NAME not in request_json_object:
        start_response('400 Bad Request', [('Content-Type', 'application/json')])
        return [b'{"error":"invalid_params","res":"no_code_embedded"}']

    headers.append(('Access-Control-Allow-Origin', origin))
    start_response('200 OK', headers)

    # execute program with timed out
    result_dict = time_out_execute(code=request_json_object[REQUEST_CODE_NAME],
                                   graph_json=request_json_object[REQUEST_GRAPH_NAME])

    return [json.dumps(result_dict).encode('utf-8')]


if __name__ == '__main__':
    try:
        main(arg_parser()['port'])
    except KeyboardInterrupt:
        print('Interrupted by keyboard.')
    except Exception as exc:
        print(f'Unknown exception occurred. Error: {exc}')
    finally:
        print('Stopped the server.')
