from django.core.handlers.wsgi import WSGIRequest

import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql.execution.base import ResolveInfo

from ..models import Category, Tutorial, Graph

from .types import UserType, CategoryType, TutorialType, GraphType


class Query(graphene.ObjectType):
    user_info = graphene.Field(UserType)
    all_categories = graphene.List(CategoryType)
    all_tutorial_info = graphene.List(TutorialType)

    tutorial = graphene.Field(TutorialType, url=graphene.String(), id=graphene.String())
    graph = graphene.Field(GraphType, url=graphene.String(), id=graphene.String())

    @login_required
    def resolve_user_info(self, info: ResolveInfo, **kwargs):
        return info.context.user

    def resolve_all_categories(self, info: ResolveInfo, **kwargs):
        return Category.objects.all()

    def resolve_all_tutorial_info(self, info: ResolveInfo, **kwargs):
        return Tutorial.objects.all()

    def resolve_tutorial(self, info: ResolveInfo, **kwargs):
        url = kwargs.get('url', None)
        idt = kwargs.get('id', None)
        if url:
            return Tutorial.objects.get(url=url)
        elif idt:
            return Tutorial.objects.get(id=idt)
        return None

    def resolve_graph(self, info: ResolveInfo, **kwargs):
        url = kwargs.get('url', None)
        idt = kwargs.get('id', None)
        if url:
            return Graph.objects.get(url=url)
        elif idt:
            return Graph.objects.get(id=idt)
        return None
