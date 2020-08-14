from graphql import ResolveInfo

from backend.model.UserModel import ROLES


# TODO a better name
def show_published_only(func):
    def wrapper(*args, **kwargs):
        user = next(arg for arg in args if isinstance(arg, ResolveInfo)).context.user
        is_published_only = user.is_anonymous or user.role < ROLES.TRANSLATOR
        result = func(is_published_only=is_published_only, *args, **kwargs)
        return result
    return wrapper
