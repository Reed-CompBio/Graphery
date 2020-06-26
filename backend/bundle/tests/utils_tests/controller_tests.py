import os
import sys
import pathlib
from importlib import import_module

import pytest
from bundle.controller import controller
from bundle.utils.cache_file_helpers import TempSysPathAdder, load_zip_file, verify_unloaded_files


@pytest.mark.parametrize('zip_file_dir, unzip_dir', [
    pytest.param(
        'simple_graph_with_degree_algorithm.zip',
        'simple_graph_with_degree_algorithm',
    )
])
def test_dump_result(zip_file_dir, unzip_dir):
    zip_file_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / 'zip_files' / zip_file_dir

    with controller as folder_creator, folder_creator(unzip_dir) as cache_folder, TempSysPathAdder(cache_folder):
        load_zip_file(zip_file_path, cache_folder.cache_folder_path)
        assert verify_unloaded_files(cache_folder.cache_folder_path)

        imported_module = import_module('entry')

        graphery_functions = [getattr(imported_module, attr_name)
                              for attr_name in [item for item in dir(imported_module)
                                                if item.startswith('graphery_')]
                              ]
        # for func in graphery_functions:
        #     result = func()

        result = graphery_functions[0]()

        del sys.modules['entry']
        del imported_module

    print(controller.processor.result)
    print(controller.processor.result_json)
