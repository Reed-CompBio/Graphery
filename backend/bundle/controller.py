import pathlib
from typing import Union

from bundle.utils.cache_file_helpers import CacheFolder, USER_DOCS_PATH
from bundle.seeker import tracer

from time import time


class Controller:
    def __init__(self, cache_path=USER_DOCS_PATH):
        self.main_cache_folder = CacheFolder(cache_path, auto_delete=False)
        self.log_folder = CacheFolder(cache_path, auto_delete=False)
        self.tracer_cls = tracer

        self.main_cache_folder.__enter__()
        self.tracer_cls.set_log_file_dir(self.log_folder.cache_folder_path)

    def get_recorded_content(self):
        return self.tracer_cls.get_recorder_change_list()

    def add_cache_folder(self, dir_name: Union[str, pathlib.Path],
                         mode: int = 0o777,
                         auto_delete: bool = True) -> 'CacheFolder':
        return self.main_cache_folder.add_cache_folder(dir_name, mode, auto_delete)

    def __enter__(self):
        self.tracer_cls.new_recorder()
        self.tracer_cls.set_log_file_name(str(time()))
        # TODO give a prompt that the current session is under this time stamp

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        self.__exit__(None, None, None)


controller = Controller()
