import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout

from backend.graphql.types import UserType
from backend.models import ROLES

require_admin = user_passes_test(lambda u: u.is_authenticated and u.role >= ROLES.AUTHOR)


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean(required=True)
    user = graphene.Field(UserType)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(info.context, user)
        return Login(success=user is not None, user=user)


class Logout(graphene.Mutation):
    success = graphene.Boolean(required=True)

    def mutate(self, info):
        user = info.context.user
        if user.is_authenticated:
            logout(info.context)
            return Login(success=True)
        else:
            raise GraphQLError('Not Logged In')


class Mutation(graphene.ObjectType):
    login = Login.Field()
    logout = Logout.Field()
