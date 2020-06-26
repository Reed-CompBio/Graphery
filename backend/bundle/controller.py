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
        self.recorder = Recorder()
        self.processor = Processor()

        self.main_cache_folder.__enter__()
        self.tracer_cls.set_log_file_dir(self.log_folder.cache_folder_path)

        self.tracer_cls.set_new_recorder(self.recorder)

    def get_recorded_content(self):
        return self.recorder.changes

    def __call__(self, dir_name: Union[str, pathlib.Path] = None,
                       mode: int = 0o777,
                       auto_delete: bool = True,
                       *args, **kwargs) -> CacheFolder:
        if dir_name:
            return self.main_cache_folder.add_cache_folder(dir_name, mode, auto_delete)
        else:
            return self.main_cache_folder

    def __enter__(self):
        self.recorder.purge()
        self.processor.purge()

        self.tracer_cls.set_log_file_name(str(time()))
        # TODO give a prompt that the current session is under this time stamp
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.processor.load_data(change_list=self.recorder.changes, variables=self.recorder.variables)
        self.processor.generate_result_json()

    def __del__(self):
        self.main_cache_folder.__exit__(None, None, None)


controller = Controller()

del Controller  # User should only have one controller
