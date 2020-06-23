from typing import Iterable

import graphene
from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql import ResolveInfo

# from ..models import User
from ..model.UserModel import ROLES
# from ..model.validators import validate
from ..models import Category, Tutorial, Graph

from .types import UserType, CategoryType, TutorialType, GraphType


class Query(graphene.ObjectType):
    # username_exist = graphene.Boolean(username=graphene.String(required=True))
    # email_exist = graphene.Boolean()
    user_info = graphene.Field(UserType)
    all_categories = DjangoListField(CategoryType)
    all_tutorial_info = DjangoListField(TutorialType)
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
    def resolve_user_info(self, info: ResolveInfo, **kwargs):
        return info.context.user

    def resolve_all_categories(self, info: ResolveInfo, **kwargs):
        return Category.objects.all()

    def resolve_all_tutorial_info(self, info: ResolveInfo, **kwargs):
        return Tutorial.objects.all()

    def resolve_tutorial_count(self, info: ResolveInfo, **kwargs):
        if info.context.user.is_anonymous or info.context.user.role < ROLES.TRANSLATOR:
            return Tutorial.objects.filter(is_published=True).count()
        return Tutorial.objects.all().count()

    def resolve_tutorial(self, info: ResolveInfo, url=None, id=None):
        raw_result: QuerySet = Tutorial.objects.all()
        if info.context.user.is_anonymous or info.context.user.role < ROLES.TRANSLATOR:
            raw_result = raw_result.filter(is_published=True)
        if url:
            return raw_result.get(url=url)
        elif id:
            return raw_result.get(id=id)

        raise GraphQLError('The tutorial you requested with url={}, id={} does not exist.'.format(url, id))

    def resolve_tutorials(self, info: ResolveInfo, category_names: Iterable = ()):
        results = QuerySet()
        for category_name in category_names:
            try:
                category = Category.objects.get(category=category_name)
                results.union(category.tutorial_set.all())
            except Category.DoesNotExist:
                raise GraphQLError('Category {} does not exist in database. The request cannot be completed'
                                   .format(category_name))
        return results

    def resolve_graph(self, info: ResolveInfo, url=None, id=None):
        raw_result: QuerySet = Graph.objects.all()
        if info.context.user.is_anonymous:
            raw_result = raw_result.filter(is_published=True)

        if url:
            return raw_result.get(url=url)
        elif id:
            return raw_result.get(id=id)
        raise GraphQLError('The graph you requested with url={}, id={} does not exist.'.format(url, id))
