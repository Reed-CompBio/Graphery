import pathlib
from typing import Union

from bundle.utils.processor import Processor
from bundle.utils.recorder import Recorder
from bundle.utils.cache_file_helpers import CacheFolder, USER_DOCS_PATH
from bundle.seeker import tracer

from time import time


class Controller:
    def __init__(self, cache_path=USER_DOCS_PATH):
        self.main_cache_folder = CacheFolder(cache_path, auto_delete=False)
        self.log_folder = CacheFolder(cache_path, auto_delete=False)
        self.tracer_cls = tracer
        self.recorder = None
        self.processor = None

        self.main_cache_folder.__enter__()
        self.tracer_cls.set_log_file_dir(self.log_folder.cache_folder_path)

    def load_new_recorder(self) -> None:
        self.recorder = Recorder()

    def get_recorded_content(self):
        return self.recorder.changes

    def load_new_processor(self) -> None:
        self.processor = Processor()

    def __call__(self, dir_name: Union[str, pathlib.Path] = None,
                       mode: int = 0o777,
                       auto_delete: bool = True,
                       *args, **kwargs) -> CacheFolder:
        if dir_name:
            return self.main_cache_folder.add_cache_folder(dir_name, mode, auto_delete)
        else:
            return self.main_cache_folder

    def __enter__(self):
        self.load_new_recorder()
        self.load_new_processor()

        self.tracer_cls.set_new_recorder(self.recorder)
        self.tracer_cls.set_log_file_name(str(time()))
        # TODO give a prompt that the current session is under this time stamp
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO process data here
        pass

    def __del__(self):
        self.main_cache_folder.__exit__(None, None, None)


controller = Controller()

del Controller  # User should only have one controller
