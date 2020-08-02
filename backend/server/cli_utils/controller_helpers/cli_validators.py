import re
import pathlib
from typing import List

from django.db.models import QuerySet
from prompt_toolkit.completion import PathCompleter

from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError


class CodeSourceFolderValidator(Validator):
    def validate(self, document: Document) -> None:
        code_path = pathlib.Path(document.text)
        entry_py_module = code_path / 'entry.py'
        graph_info = code_path / 'graph-info.json'
        if not code_path.exists() or not entry_py_module.exists() or not graph_info.exists():
            raise ValidationError(message='The code resources folder does not exist or does not contain'
                                          ' an `entry.py` file and a `graph-info.json` file.')


class NameValidator(Validator):
    regex = re.compile(r'^[a-zA-Z0-9- ]+\Z')

    def __init__(self):
        super().__init__()
        self.names: List[str] = []

    def __call__(self, tutorials: QuerySet = ()) -> Validator:
        for element in tutorials:
            self.names.append(element.name)
        return self

    def validate(self, document: Document) -> None:
        name = document.text.strip()
        if not self.regex.match(name):
            raise ValidationError(message='The name is not valid. '
                                          'It should only contain letters, numbers, dashes, and spaces.',
                                  cursor_position=len(name) - 1)
        if name in self.names:
            raise ValidationError(message='The name {} is taken. Please enter a new name!'.format(name),
                                  cursor_position=len(name) - 1)


class UrlValidator(Validator):
    regex = re.compile(r'^[a-zA-Z0-9-]+\Z')

    def __init__(self):
        super().__init__()
        self.urls: List[str] = []

    def __call__(self, tutorials: QuerySet) -> Validator:
        for element in tutorials:
            self.urls.append(element.url)
        return self

    def validate(self, document: Document) -> None:
        url = document.text.strip()
        if not self.regex.match(url):
            raise ValidationError(message='The url is not valid'
                                          'It should only contain letters, numbers and dashes.',
                                  cursor_position=len(url) - 1)
        if url in self.urls:
            raise ValidationError(message='The url {} is taken. Please enter a new url!'.format(url),
                                  cursor_position=len(url) - 1)


class LocationValidator(Validator):
    def validate(self, document: Document) -> None:
        if not pathlib.Path(document.text).exists():
            raise ValidationError(message='Please input a valid path!')


class EmailValidator(Validator):
    regex = re.compile(r'^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]+$')

    def validate(self, document: Document) -> None:
        if not self.regex.match(document.text):
            raise ValidationError(message='The email format is not valid')


class UsernameValidator(Validator):
    regex = re.compile(r'^[^0-9][\w-]{4,}[^-_]\Z')

    def validate(self, document: Document) -> None:
        if len(document.text) < 6:
            raise ValidationError(message='Username must be at least 6 letters long')
        if not self.regex.match(document.text):
            raise ValidationError(message='Username only contains letters, numbers, and /-/_ characters.')


class PasswordValidator(Validator):
    def validate(self, document: Document) -> None:
        # TODO write password validation
        if len(document.text) < 8:
            raise ValidationError(message='The length of the password must be greater than 8')
        if len(document.text) > 20:
            raise ValidationError(message='The length of the password must be smaller than 20')


class ServerPathValidator(Validator):
    def validate(self, document: Document) -> None:
        path = pathlib.Path(document.text)
        if path.exists() and (path / 'manage.py').exists():
            pass
        else:
            raise ValidationError(
                message='The server location you provided {} is not valid'.format(str(path)),
                cursor_position=len(document.text) - 1)


class BundlePathValidator(Validator):
    def validate(self, document: Document) -> None:
        path = pathlib.Path(document.text)
        if path.exists() and (path / 'bundle').exists():
            pass
        else:
            raise ValidationError(message='Please enter the parent folder where bundle src live')


server_path_validator = ServerPathValidator()
bundle_validator = BundlePathValidator()

path_completer = PathCompleter()
name_validator = NameValidator()
url_validator = UrlValidator()
location_validator = LocationValidator()
code_source_folder_validator = CodeSourceFolderValidator()
email_validator = EmailValidator()
username_validator = UsernameValidator()
password_validator = PasswordValidator()
