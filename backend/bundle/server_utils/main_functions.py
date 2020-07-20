import json
from typing import Mapping, Callable
from wsgiref.simple_server import make_server
from multiprocessing import Pool, TimeoutError

from bundle.server_utils.params import TIMEOUT_SECONDS, REQUEST_CODE_NAME, ONLY_ACCEPTED_ORIGIN, ACCEPTED_ORIGIN, \
    REQUEST_GRAPH_NAME
from bundle.server_utils.utils import create_error_response, create_data_response, execute, \
    ExecutionException


def main(port: int):
    with make_server('127.0.0.1', port, application) as httpd:
        print('Press <ctrl+c> to stop the server. ')
        print(f'Ready for Python code on port {port} ...')
        httpd.serve_forever()


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


def application_helper(environ: Mapping) -> Mapping:
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')

    # info page
    if method == 'GET' and path == '/env':
        return create_data_response(environ)

    # entry point check
    if method != 'POST' or path != '/run':
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
