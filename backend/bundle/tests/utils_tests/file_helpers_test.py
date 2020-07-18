import pathlib
import os
import sys
from importlib import import_module
import textwrap

import pytest
import bundle.utils.cache_file_helpers as file_helper

DEFAULT_CACHE_FOLDER = file_helper.USER_DOCS_PATH


@pytest.fixture
def lv1_cache_folder():
    with file_helper.CacheFolder() as cache_folder:
        yield cache_folder


@pytest.fixture
def get_fixture(request):
    def _get_fixture(name):
        return request.getfixturevalue(name)

    return _get_fixture


@pytest.mark.parametrize('folder_dir, expected', [
    pytest.param('graphery_folder_test', str(DEFAULT_CACHE_FOLDER / 'graphery_folder_test')),
])
def test_cache_folder_naming(lv1_cache_folder, folder_dir, expected):
    with lv1_cache_folder.add_cache_folder(folder_dir) as cache_folder:
        assert str(cache_folder.cache_folder_path) == expected


@pytest.mark.parametrize('base_folder, dir_name, expected_full_dir', [
    pytest.param('lv1_cache_folder',
                 'c_folder',
                 str(DEFAULT_CACHE_FOLDER / 'c_folder')
                 ),
    pytest.param('lv1_cache_folder',
                 'c_folder/lv2cache_folder',
                 str(DEFAULT_CACHE_FOLDER / 'c_folder/lv2cache_folder'),
                 marks=pytest.mark.xfail
                 ),
])
def test_cache_folder_generating(get_fixture, base_folder, dir_name, expected_full_dir):
    with get_fixture(base_folder).add_cache_folder(dir_name) as next_lv_dir:
        assert str(next_lv_dir.cache_folder_path) == expected_full_dir


@pytest.mark.parametrize('auto_remove', [False, True])
def test_cache_folder_auto_delete(auto_remove):
    with file_helper.CacheFolder(auto_delete=auto_remove) as cache_folder:
        assert cache_folder.exists()
    assert cache_folder.exists() ^ auto_remove


@pytest.mark.parametrize('lv2dirs, auto_rms, expected_dir', [
    pytest.param(
        ['c_folder'],
        [True],
        str(DEFAULT_CACHE_FOLDER)
    ),
    pytest.param(
        ['c_folder', 'this_is_md5_hash', 'result'],
        [True, False, True],
        str(DEFAULT_CACHE_FOLDER),
        marks=pytest.mark.xfail(reason='The second folder does not have a parent folder')
    ),
    pytest.param(
        ['c_folder', 'this_is_md5_hash', 'result'],
        [False, True, True],
        str(DEFAULT_CACHE_FOLDER / 'c_folder' / 'this_is_md5_hash'),
        marks=pytest.mark.xfail(reason='The folder is auto deleted')
    ),
    pytest.param(
        ['c_folder', 'this_is_md5_hash', 'result'],
        [False, False, True],
        str(DEFAULT_CACHE_FOLDER / 'c_folder' / 'this_is_md5_hash')
    )
])
def test_multiple_level_folder_auto_delete(lv1_cache_folder, lv2dirs, auto_rms, expected_dir):
    path = lv1_cache_folder.cache_folder_path
    for i in range(len(lv2dirs)):
        lv2dirs[i] = path / lv2dirs[i]
        path = lv2dirs[i]

    for path, auto_rm in zip(lv2dirs, auto_rms):
        with lv1_cache_folder.add_cache_folder(path, auto_delete=auto_rm) as cache_folder:
            assert cache_folder.exists()

        assert cache_folder.exists() ^ auto_rm

    assert pathlib.Path(expected_dir).exists()


@pytest.mark.parametrize('dir_path, dir_auto_delete, file_name, content', [
    pytest.param(
        'f29c8a70d54c012df8b7e1923ca55998',
        True,
        'f29c8a70d54c012df8b7e1923ca55998',
        'These violent delights have violent ends'
    ),
    pytest.param(
        '1cf2b70475e0eaca37b6314c9a016a1d',
        False,
        '1cf2b70475e0eaca37b6314c9a016a1d',
        '166826574942457936796479153347633964941'
    )
])
def test_write_and_import_temp_file(lv1_cache_folder, dir_path, dir_auto_delete, file_name, content):
    with lv1_cache_folder.add_cache_folder(dir_path, auto_delete=dir_auto_delete) as cache_folder, \
            file_helper.TempSysPathAdder(cache_folder):
        py_file_path = cache_folder.cache_folder_path / ('%s.py' % file_name)
        file_content = textwrap.dedent(u"""
            from bundle.utils.cache_file_helpers import get_md5_of_a_string 
            content = '%s'
            md5_content = get_md5_of_a_string(content)
        """ % content)

        with py_file_path.open('w') as py_file:
            py_file.write(file_content)

        assert py_file_path.exists()

        imported_module = import_module(file_name)

        assert 'content' in imported_module.__dict__
        assert imported_module.content == content

        assert 'md5_content' in imported_module.__dict__
        assert imported_module.md5_content == imported_module.__name__

    assert cache_folder.exists() ^ dir_auto_delete and py_file_path.exists() ^ dir_auto_delete


@pytest.mark.parametrize('zip_file_dir, unzip_dir, files, attrs', [

    pytest.param(
        'simple_nodes_no_graphs.zip',
        'simple_nodes_no_graphs',
        ['entry.py', 'graph.json'],
        ['node_id_list', 'node_list']
    ),
    pytest.param(
        'simple_entry_no_graphs.zip',
        'simple_entry_no_graphs',
        ['entry.py', 'graph.json'],
        ['md5_content']
    ),
    pytest.param(
        'simple_edges_no_graphs.zip',
        'simple_edges_no_graphs',
        ['entry.py', 'graph.json'],
        ['node_list', 'edge_list']
    ),
    pytest.param(
        'simple_graph.zip',
        'simple_graph',
        ['entry.py', 'graph.json'],
        ['graph']
    ),
    pytest.param(
        'simple_graph_with_degree_algorithm.zip',
        'simple_graph_with_degree_algorithm',
        ['entry.py', 'graph.json', 'supply.py'],
        ['graphery_count_degree_by_nodes', 'graphery_count_degree_by_edges']
    )

])
def test_unzip_and_import_entry(lv1_cache_folder, zip_file_dir, unzip_dir, files, attrs):
    zip_file_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / 'zip_files' / zip_file_dir
    with lv1_cache_folder.add_cache_folder(unzip_dir) as folder, \
            file_helper.TempSysPathAdder(folder):
        file_helper.load_zip_file(zip_file_path, folder.cache_folder_path)
        for file in files:
            assert (folder.cache_folder_path / file).exists()

        imported_module = import_module('entry')
        for attr_name in attrs:
            assert hasattr(imported_module, attr_name)

        del sys.modules['entry']


@pytest.mark.parametrize('zip_file_dir, unzip_dir, entries, expected_result', [
    pytest.param(
        'simple_graph_with_degree_algorithm.zip',
        'simple_graph_with_degree_algorithm',
        ['graphery_count_degree_by_nodes', 'graphery_count_degree_by_edges'],
        []
    )
])
def test_run_import(lv1_cache_folder, zip_file_dir, unzip_dir, entries, expected_result):
    zip_file_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / 'zip_files' / zip_file_dir
    with lv1_cache_folder.add_cache_folder(unzip_dir) as folder, \
            file_helper.TempSysPathAdder(folder):
        file_helper.load_zip_file(zip_file_path, folder.cache_folder_path)
        assert file_helper.verify_unloaded_files(folder.cache_folder_path)

        imported_module = import_module('entry')

        graphery_functions = [getattr(imported_module, attr_name)
                              for attr_name in [item for item in dir(imported_module)
                                                if item.startswith('graphery_')]
                              ]
        # graphery_functions = [getattr(imported_module, name) for name in entries]

        assert len(graphery_functions) == len(entries)
        for func in graphery_functions:
            assert func.__name__ in entries
            result = func()
            # assert str(result) == getattr(imported_module, 'expected_dict')
            print(result)

        # IMPORTANT! remember to remove module in the end
        del sys.modules['entry']


def test_import_not_found_err(lv1_cache_folder):
    with lv1_cache_folder.add_cache_folder('err_test') as folder, file_helper.TempSysPathAdder(folder):
        file_helper.load_zip_file(pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
                                  / 'zip_files' / 'import_err.zip', folder.cache_folder_path)
        assert file_helper.verify_unloaded_files(folder.cache_folder_path)
        with pytest.raises(ModuleNotFoundError):
            import_module('entry')
