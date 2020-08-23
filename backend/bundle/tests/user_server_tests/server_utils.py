import json
from collections import Mapping
from typing import Union

from server_utils.params import VERSION


class Env:
    def __init__(self, **kwargs):
        self.content = kwargs

    def add_content(self, mapping: Mapping, **kwargs) -> 'Env':
        self.content.update(**kwargs, **mapping)
        return self


class FileLikeObj:
    def __init__(self, message):
        self.message: str = message

    def read(self, *args, **kwargs) -> str:
        print(args, kwargs)
        return self.message


def generate_wsgi_input(code: str, graph: Union[str, Mapping]):
    return FileLikeObj(json.dumps({
        'code': code,
        'graph': graph,
        'version': VERSION
    }))
