#!/usr/bin/env python3

import sys
import os
import json
import subprocess
import tempfile
from urllib import parse
from wsgiref.simple_server import make_server


def valid_version():
    v = sys.version_info
    if v.major == 3 and v.minor >= 4:
        return True
    print('Your current python is %d.%d. Please use Python 3.4.' % (v.major, v.minor))
    return False


if not valid_version():
    exit(1)


EXEC = sys.executable
PORT = 39093
HOST = 'localhost:%d' % PORT
# TODO 牛逼！
TEMP = tempfile.mkdtemp(suffix='_py', prefix='learn_python_')
INDEX = 0


def main():
    httpd = make_server('127.0.0.1', PORT, application)
    print('Ready for Python code on port %d...' % PORT)
    httpd.serve_forever()


def get_name():
    global INDEX
    INDEX = INDEX + 1
    return 'test_%d' % INDEX


def write_py(name, code):
    fpath = os.path.join(TEMP, '%s.py' % name)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(code)
    print('Code wrote to: %s' % fpath)
    return fpath


def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        # TODO utf-8 should be the only valid encoding. Pass error to the frontend when
        #  the encoding error is encountered
        return s.decode('gbk')


def application(environ, start_response):
    host = environ.get('HTTP_HOST')
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')
    if method == 'GET' and path == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [
            b'<html><head><title>Learning Python</title></head><body><form method="post" action="/run"><textarea name="code" style="width:90%;height: 600px"></textarea><p><button type="submit">Run</button></p></form></body></html>']
    if method == 'GET' and path == '/env':
        start_response('200 OK', [('Content-Type', 'text/html')])
        L = [b'<html><head><title>ENV</title></head><body>']
        for k, v in environ.items():
            p = '<p>%s = %s' % (k, str(v))
            L.append(p.encode('utf-8'))
        L.append(b'</html>')
        return L
    if host != HOST or method != 'POST' or path != '/run' or not environ.get('CONTENT_TYPE', '').lower().startswith(
            'application/x-www-form-urlencoded'):
        start_response('400 Bad Request', [('Content-Type', 'application/json')])
        return [b'{"error":"bad_request","res":"wrong_method"}']
    s = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    qs = parse.parse_qs(s.decode('utf-8'))
    if not 'code' in qs:
        start_response('400 Bad Request', [('Content-Type', 'application/json')])
        return [b'{"error":"invalid_params","res":"no_code_embedded"}']
    name = qs['name'][0] if 'name' in qs else get_name()
    code = qs['code'][0]
    headers = [('Content-Type', 'application/json')]
    origin = environ.get('HTTP_ORIGIN', '')
    # if origin.find('.liaoxuefeng.com') == -1:
    # start_response('400 Bad Request', [('Content-Type', 'application/json')])
    # return [b'{"error":"invalid_origin"}']
    headers.append(('Access-Control-Allow-Origin', origin))
    start_response('200 OK', headers)
    r = dict()
    try:
        fpath = write_py(name, code)
        print('Execute: %s %s' % (EXEC, fpath))
        r['output'] = decode(subprocess.check_output([EXEC, fpath], stderr=subprocess.STDOUT, timeout=5))
    except subprocess.CalledProcessError as e:
        r = dict(error='Exception', output=decode(e.output))
    except subprocess.TimeoutExpired as e:
        r = dict(error='Timeout', output='执行超时')
    except subprocess.CalledProcessError as e:
        r = dict(error='Error', output='执行错误')
    print('Execute done.')
    return [json.dumps(r).encode('utf-8')]


if __name__ == '__main__':
    main()

