import graphene
import graphql_jwt
from graphql_jwt.decorators import user_passes_test

from backend.graphql.types import UserType
from backend.models import ROLES

require_admin = user_passes_test(lambda u: u.is_authenticated and u.role >= ROLES.AUTHOR)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
