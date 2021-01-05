import logging
from functools import wraps

from graphql import ResolveInfo, GraphQLError

# Modified from django-graphql-jwt
from backend.model.UserModel import ROLES

api_logger = logging.getLogger('django.api')


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = next(arg for arg in args if isinstance(arg, ResolveInfo))
            return func(info.context, *args, **kwargs)

        return wrapper

    return decorator


def user_passes_test(test_func, exc=GraphQLError('You do not have permission to perform this action')):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(request_context, *args, **kwargs):
            if test_func(request_context.user):
                return f(*args, **kwargs)
            api_logger.error(f'The error is caused by illegally accessing method: {f.__qualname__}, '
                             f'determined by test: {test_func.__qualname__}.')
            raise exc

        return wrapper

    return decorator


def is_anonymous(u):
    return not u.is_authenticated


def is_authenticated(u):
    return u.is_authenticated


def has_write_permission(u):
    return u.is_authenticated and u.role > ROLES.TRANSLATOR


def is_admin(u):
    return u.is_authenticated and u.role == ROLES.ADMINISTRATOR


anonymous_required = user_passes_test(is_anonymous,
                                      GraphQLError('You can not perform this action while logged in.'))

login_required = user_passes_test(is_authenticated,
                                  GraphQLError('Login required to perform this action.'))

write_required = user_passes_test(has_write_permission,
                                  GraphQLError('You must have write permission to perform this action.'))

admin_required = user_passes_test(is_admin,
                                  GraphQLError('You must have admin privilege to perform this action.'))
