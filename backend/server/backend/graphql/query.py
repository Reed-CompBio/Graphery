from typing import Iterable

import graphene
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import GraphQLError
from graphql import ResolveInfo

from .decorators import login_required
from ..model.filters import show_published_only
from ..model.translation_collection import translation_tables
from ..models import Category, Tutorial, Graph, ExecResultJson

from .types import UserType, CategoryType, TutorialType, GraphType, Code, ExecResultJsonType, CodeType


class Query(graphene.ObjectType):
    # username_exist = graphene.Boolean(username=graphene.String(required=True))
    # email_exist = graphene.Boolean()
    user_info = graphene.Field(UserType)
    all_categories = DjangoListField(CategoryType)
    all_tutorial_info = DjangoListField(TutorialType)
    all_graph_info = DjangoListField(GraphType)
    all_code = DjangoListField(CodeType)
    all_exec_result = DjangoListField(ExecResultJsonType)
    all_supported_lang = graphene.List(graphene.String)
    tutorial_count = graphene.Int()

    tutorial = graphene.Field(TutorialType,
                              url=graphene.String(),
                              id=graphene.String())
    tutorials = DjangoListField(TutorialType,
                                         categoryies=graphene.List(graphene.String))
    graph = graphene.Field(GraphType,
                           url=graphene.String(),
                           id=graphene.String())

    # The most efficient method of finding whether a model with a unique field is a member of a QuerySet
    # def resolve_username_exist(self, info, username):
    #     return User.objects.filter(username=username).exists()

    # def resolve_email_exist(self, info, email):
    #     return User.objects.filter(email=email).exists()

    @login_required
    def resolve_user_info(self, info: ResolveInfo):
        return info.context.user

    def resolve_all_categories(self, info: ResolveInfo):
        return Category.objects.all()

    def resolve_all_tutorial_info(self, info: ResolveInfo):
        return Tutorial.objects.all()

    def resolve_all_graph_info(self, info: ResolveInfo):
        return Graph.objects.all()

    @login_required
    def resolve_all_code(self, info: ResolveInfo):
        return Code.objects.all()

    @login_required
    def resolve_all_exec_result(self, info: ResolveInfo):
        return ExecResultJson.objects.all()

    def resolve_all_supported_lang(self, info: ResolveInfo):
        return translation_tables

    @show_published_only
    def resolve_tutorial_count(self, info: ResolveInfo, is_published_only: bool, **kwargs):
        return Tutorial.objects.is_published_only_all(is_published_only=is_published_only).count()

    @show_published_only
    def resolve_tutorial(self, info: ResolveInfo, is_published_only: bool, url=None, id=None):
        raw_result: QuerySet = Tutorial.objects.is_published_only_all(is_published_only=is_published_only)

        try:
            if url:
                return raw_result.get(url=url)
            elif id:
                return raw_result.get(id=id)
        except Tutorial.DoesNotExist:
            raise GraphQLError('The tutorial you requested with url={}, id={} does not exist.'.format(url, id))

        raise GraphQLError('In tutorial query, the url and id arguments can not both be empty.')

    @show_published_only
    def resolve_tutorials(self, info: ResolveInfo, is_published_only: bool, categories: Iterable = ()):
        return Category.objects.is_published_only_all(is_published_only=is_published_only)\
                               .filter(category_in=categories)

    @show_published_only
    def resolve_graph(self, info: ResolveInfo, is_published_only: bool, url=None, id=None):
        raw_result: QuerySet = Graph.objects.is_published_only_all(is_published_only=is_published_only)

        if url:
            return raw_result.get(url=url)
        elif id:
            return raw_result.get(id=id)
        raise GraphQLError('The graph you requested with url={}, id={} does not exist.'.format(url, id))
