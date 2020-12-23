import pathlib
from typing import Union, List, Mapping

from bundle.utils.recorder import Recorder
from bundle.utils.cache_file_helpers import CacheFolder, USER_DOCS_PATH
from bundle.seeker import tracer

from time import time


class _Controller:
    def __init__(self, cache_path=USER_DOCS_PATH, auto_delete: bool = False):
        self.main_cache_folder = CacheFolder(cache_path, auto_delete=auto_delete)
        self.log_folder = CacheFolder(cache_path / 'log', auto_delete=auto_delete)
        # TODO think about this, and the log file location in the sight class
        self.log_folder.mkdir(parents=True, exist_ok=True)
        self.tracer_cls = tracer
        self.recorder = Recorder()

        self.main_cache_folder.__enter__()
        self.tracer_cls.set_log_file_dir(self.log_folder.cache_folder_path)

        self.tracer_cls.set_new_recorder(self.recorder)

    def get_recorded_content(self) -> List[Mapping]:
        return self.recorder.get_change_list()

    def get_processed_result(self) -> List[Mapping]:
        return self.recorder.get_change_list()

    def get_processed_result_json(self) -> str:
        return self.recorder.get_change_list_json()

    def purge_records(self):
        self.recorder.purge()

    def generate_processed_record(self):
        raise DeprecationWarning()

    def __call__(self, dir_name: Union[str, pathlib.Path] = None,
                       mode: int = 0o777,
                       auto_delete: bool = False,
                       *args, **kwargs) -> CacheFolder:
        if dir_name:
            return self.main_cache_folder.add_cache_folder(dir_name, mode, auto_delete)
        else:
            return self.main_cache_folder

    def __enter__(self):
        self.tracer_cls.set_log_file_name(f'{time()}.log')
        # TODO give a prompt that the current session is under this time stamp
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tracer_cls.set_log_file_name(None)

    def __del__(self):
        self.main_cache_folder.__exit__(None, None, None)


controller = _Controller()
