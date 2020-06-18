from django.core.handlers.wsgi import WSGIRequest

import graphene
from graphql_jwt.decorators import login_required
from graphql.execution.base import ResolveInfo

from ..models import Category, Tutorial

from .types import UserType, CategoryType, TutorialType


class Query(graphene.ObjectType):
    user_info = graphene.Field(UserType)
    all_categories = graphene.List(CategoryType)
    all_tutorial_info = graphene.List(TutorialType)

    @login_required
    def resolve_user_info(self, info: ResolveInfo, **kwargs):
        return info.context.user

    def resolve_all_categories(self, info: ResolveInfo, **kwargs):
        return Category.objects.all()

    def resolve_all_tutorial_info(self, info: ResolveInfo, **kwargs):
        return Tutorial.objects.all()
