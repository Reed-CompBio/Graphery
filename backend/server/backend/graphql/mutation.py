import graphene
from graphql import GraphQLError
from django.contrib.auth import authenticate, login, logout

from backend.graphql.admin_mutations import UpdateCategory, UpdateTutorialAnchor, UpdateGraph
from backend.graphql.types import UserType


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
    update_category = UpdateCategory.Field()
    update_tutorial_anchor = UpdateTutorialAnchor.Field()
    update_graph = UpdateGraph.Field()
