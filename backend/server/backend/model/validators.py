from types import FunctionType
from typing import Callable, Iterable

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from graphql import GraphQLError


class UserNameValidator(RegexValidator):
    # require the length of the user name be at least 6
    regex = r'^[^0-9][\w-]{4,}[^-_]\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and /-/_ characters.'
        'The length should be at least 6 characters'
        'The username should not start with a number of end with _/-'
    )


def validate(validators: Iterable[Callable] = ()) -> FunctionType:
    def wrapper_func(func):
        def wrapper(*args, **kwargs):
            for validator in validators:
                flag, message = validator(*args, **kwargs)
                if not flag:
                    raise GraphQLError(f'Validation not passed: {message}')

            return func(*args, **kwargs)
        return wrapper

    return wrapper_func
