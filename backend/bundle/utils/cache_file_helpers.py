"""
cache file helpers
"""

import sys
import shutil
import contextlib
import pathlib
from random import getrandbits
from hashlib import md5
from typing import Union
from zipfile import ZipFile

USER_DOCS_PATH: pathlib.Path = pathlib.Path.home() / 'Documents' / '.graphery_cache'


class TempSysPathAdder:
    """
    Context manager for temporarily adding paths to `sys.path`.

    Removes the path(s) after suite.

    Example::

        with TempSysPathAdder('path/to/fubar/package'):
            import fubar
            fubar.do_stuff()

    """
    def __init__(self, addition: Union['CacheFolder', pathlib.Path]):
        if isinstance(addition, CacheFolder):
            self.addition = [str(addition.cache_folder_path)]
        elif isinstance(addition, pathlib.Path):
            self.addition = [str(addition)]

    def __enter__(self):
        self.entries_not_in_sys_path = [entry for entry in self.addition if
                                        entry not in sys.path]
        sys.path += self.entries_not_in_sys_path
        return self

    def __exit__(self, *args, **kwargs):

        for entry in self.entries_not_in_sys_path:

            # We don't allow anyone to remove it except for us:
            assert entry in sys.path

            sys.path.remove(entry)


class CacheFolder(contextlib.AbstractContextManager):
    """
    Create a cache folder directory and delete it after exiting the context if auto-delete is set to True

    Usage::
        with CacheFolder(cache_folder=cache_folder_path, folder_mode=0o777, auto_delete=True) as cache_dir:
            # We have a temporary folder!
            assert cache_folder.is_dir()

            # We can create files in it:
            (temp_folder / 'my_file').open('w')

            # blah blah do something!
            ...

        # The suite is finished, now it's all cleaned:
        assert not cache_folder.exists()

    With temp system added, you can add the cache folder to sys.path
    so that the program can import caches files inside of the folder::

        from importlib import import_module
        with CacheFolder(dir, mode, delete_flag) as cache_folder, \
                TempSysPathAdder(str(cache_folder.cache_folder_path)):
            file_name = 'blah_blah'
            temp_file_path = cache_folder / ('%.py' % file_name)
            content = 'blah_blah_blah'
            with temp_file_path.open('w') as python_file:
                python_file.write(content)
            module = import_module(module_name)
            # do some stuff with the module

    Logic: There should be a first_level cache folder where all the cache files
           and folders should be it's children. When you want to access a folder,
           you have to use `with` clause so that the folder will be created and
           deleted if the auto_delete flag is set to true. Cache files in side of
           cache folder are not deleted automatically.
    """

    def __init__(self, cache_folder: pathlib.Path = USER_DOCS_PATH,
                 folder_mode: int = 0o777,
                 auto_delete: bool = True):
        super().__init__()
        self.cache_folder_path: pathlib.Path = cache_folder
        self.folder_mode: int = folder_mode
        self.auto_delete: bool = auto_delete

    def __enter__(self) -> 'CacheFolder':
        try:
            pathlib.Path.mkdir(self.cache_folder_path, mode=self.folder_mode, parents=True, exist_ok=True)
        except FileExistsError:
            # this should not be called
            # but hmmm if the last path component is not an existing non-directory file,
            # there still will be an error, TODO I will add a logger/notification
            pass
        except FileNotFoundError:
            # every cache folder must have an parent.
            raise AssertionError('Parent Folder Does NOT Exists')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auto_delete:
            self.delete_cache_folder()

    def __str__(self):
        return 'CacheFolder <%s>' % self.cache_folder_path

    def __repr__(self):
        return self.__str__()

    def exists(self) -> bool:
        return self.cache_folder_path.exists()

    def delete_cache_folder(self):
        if self.exists():
            shutil.rmtree(self.cache_folder_path)

    def add_cache_folder(self, dir_name: Union[str, pathlib.Path],
                         mode: int = 0o777,
                         auto_delete: bool = True) -> 'CacheFolder':
        return CacheFolder(self.cache_folder_path / dir_name, folder_mode=mode, auto_delete=auto_delete)


def get_random_number_string(bits: int = 128) -> int:
    return getrandbits(bits)


def get_md5_of_a_string(text) -> str:
    return md5(str(text).encode('utf-8')).hexdigest()


def load_zip_file(zip_dir: pathlib.Path, unzip_dir: pathlib.Path) -> None:
    with ZipFile(zip_dir) as zip_file:
        zip_file.extractall(unzip_dir)


def verify_unloaded_files(unzip_dir: pathlib.Path) -> bool:
    # TODO write a more specific verification
    return (unzip_dir / 'entry.py').exists()
