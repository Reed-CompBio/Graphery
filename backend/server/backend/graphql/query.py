from typing import Iterable

import graphene
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql import ResolveInfo

from ..model.filters import show_published
from ..models import Category, Tutorial, Graph

from .types import UserType, CategoryType, TutorialType, GraphType


class Query(graphene.ObjectType):
    # username_exist = graphene.Boolean(username=graphene.String(required=True))
    # email_exist = graphene.Boolean()
    user_info = graphene.Field(UserType)
    all_categories = DjangoListField(CategoryType)
    all_tutorial_info = DjangoListField(TutorialType)
    all_graph_info = DjangoListField(GraphType)
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

    @show_published
    def resolve_tutorial_count(self, info: ResolveInfo, is_published_only: bool, **kwargs):
        if is_published_only:
            return Tutorial.objects.filter(is_published=True).count()
        return Tutorial.objects.all().count()

    @show_published
    def resolve_tutorial(self, info: ResolveInfo, is_published_only: bool, url=None, id=None):
        raw_result: QuerySet = Tutorial.objects.all()
        if is_published_only:
            raw_result = raw_result.filter(is_published=True)
        try:
            if url:
                return raw_result.get(url=url)
            elif id:
                return raw_result.get(id=id)
        except Tutorial.DoesNotExist:
            raise GraphQLError('The tutorial you requested with url={}, id={} does not exist.'.format(url, id))

        raise GraphQLError('In tutorial query, the url and id arguments can not both be empty.')

    @show_published
    def resolve_tutorials(self, info: ResolveInfo, is_published_only: bool, categoryies: Iterable = ()):
        results = Tutorial.objects.none()
        for category_name in categoryies:
            try:
                category = Category.objects.get(category=category_name)
                if category.is_published or not is_published_only:
                    results = results | category.tutorial_set.all()
            except Category.DoesNotExist:
                raise GraphQLError('Category {} does not exist in database. The request cannot be completed'
                                   .format(category_name))

        return results

    @show_published
    def resolve_graph(self, info: ResolveInfo, is_published_only: bool, url=None, id=None):
        print(info)
        raw_result: QuerySet = Graph.objects.all()
        if is_published_only:
            raw_result = raw_result.filter(is_published=True)

        if url:
            return raw_result.get(url=url)
        elif id:
            return raw_result.get(id=id)
        raise GraphQLError('The graph you requested with url={}, id={} does not exist.'.format(url, id))
