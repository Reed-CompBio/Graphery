from collections import Mapping


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
