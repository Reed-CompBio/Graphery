import graphene
import graphql_jwt
from graphql_jwt.decorators import user_passes_test

from backend.models import ROLES

require_admin = user_passes_test(lambda u: u.is_authenticated and u.role >= ROLES.AUTHOR)


# class CategoryMutation(graphene.Mutation):
#     class Arguments:
#         url =


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
