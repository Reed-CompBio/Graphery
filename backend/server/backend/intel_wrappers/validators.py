import json
import re
from typing import Sequence, Mapping, Union


class ValidationError(AssertionError):
    pass


def dummy_validator(info):
    return info


def is_published_validator(val: bool):
    if not isinstance(val, bool):
        raise ValidationError('`is_published` must be a boolean variable!')


category_regex = re.compile(r'^[^-][\w -]*[^-]$')


def category_validator(val: str):
    if not isinstance(val, str) or not val or not category_regex.match(val):
        raise ValidationError('`category` must be a non-empty string and does not start or end with `-` or `_`.')


name_regex = re.compile(r'^[a-zA-Z0-9- ]+\Z')


def name_validator(name: str):
    if not isinstance(name, str) or not name or not name_regex.match(name):
        raise ValidationError('`name` must be a non-empty string and does not start or end with `-` or `_`.')


url_regex = re.compile(r'^[^-][a-zA-Z0-9-]*[^-]\Z')


def url_validator(url: str):
    if not isinstance(url, str) or not url or not url_regex.match(url):
        raise ValidationError('`URL must be a non-empty string containing only letters, numbers, and `-`. '
                              'It should not start or end with `-`')


def wrapper_validator(wrapper):
    wrapper.validate()


def categories_validator(cats: Sequence):
    if not isinstance(cats, Sequence):
        raise ValidationError('`Categories` must be wrapped in wrappers.')
    for cat in cats:
        wrapper_validator(cat)


def authors_validator(authors: Sequence):
    if not isinstance(authors, Sequence):
        raise ValidationError('`authors must be wrapped in wrappers')
    for author in authors:
        wrapper_validator(author)


def code_validator(code: str):
    if not isinstance(code, str):
        raise ValidationError('`code` must be string type')


def non_empty_text_validator(text: str):
    if not isinstance(text, str) or not text.strip():
        raise ValidationError('`abstract` must be a non-empty string.')


def graph_priority_validator(priority: int):
    if priority not in {60, 40, 20}:
        raise ValidationError(f'`GraphPriority` {priority} is not valid.')


def json_validator(js: Union[str, Mapping, Sequence]):
    if isinstance(js, str):
        try:
            json.loads(js)
        except Exception as e:
            raise ValidationError(f'JSON string is not valid. Error: {e}')
    elif not isinstance(js, (Mapping, Sequence)):
        raise ValidationError('JSON must a string, a mapping, or a sequence.')


email_regex = re.compile(r'^[\w.-]+@[\w.-]+.\w{2,}$')


def email_validator(email: str):
    if not isinstance(email, str) or not email_regex.match(email):
        raise ValidationError('Email %s is not valid.' % email)


username_regex = re.compile(r'^[^0-9][\w-]{4,}[^-_]\Z')


def username_validator(username: str):
    if not isinstance(username, str) or not username_regex.match(username):
        raise ValidationError('Username %s is not valid.' % username)


password_regex = re.compile(r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$^&*])[\w\d!@#$^&*]{6,25}$')

FAKE_PASSWORD = 'Password1!'


def password_validator(password: str):
    if not isinstance(password, str) or not password_regex.match(password):
        raise ValidationError('Password %s is not valid. A valid password must contain '
                              'least one upper case, lower case of letters, '
                              'one number, AND one special character (!@#$^&*). '
                              'The length should be between 8 to 25' % password)
