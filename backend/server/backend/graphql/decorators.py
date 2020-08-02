from functools import wraps

from graphql import ResolveInfo, GraphQLError


# Copied from django-graphql-jwt
from backend.model.UserModel import ROLES


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
            raise exc
        return wrapper
    return decorator


anonymous_required = user_passes_test(lambda u: u.is_anonymous)

login_required = user_passes_test(lambda u: u.is_authenticated)

write_required = user_passes_test(lambda u: u.is_authenticated and u.role > ROLES.TRANSLATOR)

admin_required = user_passes_test(lambda u: u.is_authenticated and u.role == ROLES.ADMINISTRATOR)
