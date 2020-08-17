import pathlib
from typing import Union, List, Mapping

from utils.processor import Processor
from utils.recorder import Recorder
from utils.cache_file_helpers import CacheFolder, USER_DOCS_PATH
from seeker import tracer

from time import time


class Controller:
    def __init__(self, cache_path=USER_DOCS_PATH, auto_delete: bool = False):
        self.main_cache_folder = CacheFolder(cache_path, auto_delete=auto_delete)
        self.log_folder = CacheFolder(cache_path / 'log', auto_delete=auto_delete)
        # TODO think about this, and the log file location in the sight class
        self.log_folder.cache_folder_path.mkdir(parents=True, exist_ok=True)
        self.tracer_cls = tracer
        self.recorder = Recorder()
        self.processor = Processor()

        self.main_cache_folder.__enter__()
        self.tracer_cls.set_log_file_dir(self.log_folder.cache_folder_path)

        self.tracer_cls.set_new_recorder(self.recorder)

    def get_recorded_content(self) -> List[Mapping]:
        return self.recorder.changes

    def get_processed_result(self) -> List[Mapping]:
        return self.processor.result

    def get_processed_result_json(self) -> str:
        return self.processor.result_json

    def purge_records(self):
        self.recorder.purge()
        self.processor.purge()

    def generate_processed_record(self):
        self.processor.load_data(change_list=self.recorder.changes, variables=self.recorder.variables)
        self.processor.generate_result_json()

    def __call__(self, dir_name: Union[str, pathlib.Path] = None,
                       mode: int = 0o777,
                       auto_delete: bool = False,
                       *args, **kwargs) -> CacheFolder:
        if dir_name:
            return self.main_cache_folder.add_cache_folder(dir_name, mode, auto_delete)
        else:
            return self.main_cache_folder

    def __enter__(self):
        self.tracer_cls.set_log_file_name(str(time()))
        # TODO give a prompt that the current session is under this time stamp
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        self.main_cache_folder.__exit__(None, None, None)


controller = Controller()

del Controller  # User should only have one controller
