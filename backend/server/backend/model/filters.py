from graphql import ResolveInfo, GraphQLError

from backend.model.UserModel import ROLES


# TODO a better name
def show_published(func):
    def wrapper(*args, **kwargs):
        # TODO ?
        info = args[1]
        if not isinstance(info, ResolveInfo):
            raise GraphQLError('Internal Error in resoling is_published_only')
        user = info.context.user
        is_published_only = user.is_anonymous or user.role < ROLES.TRANSLATOR
        result = func(is_published_only=is_published_only, *args, **kwargs)
        return result
    return wrapper
