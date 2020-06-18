from django.core.handlers.wsgi import WSGIRequest

import graphene
from graphql_jwt.decorators import login_required
from graphql.execution.base import ResolveInfo

from ..model.trans_list import get_translation_table
from ..models import Category, Tutorial, Graph

from .types import UserType, CategoryType, TutorialType, GraphType
from .types import TransType


class Query(graphene.ObjectType):
    user_info = graphene.Field(UserType)
    all_categories = graphene.List(CategoryType)
    all_tutorial_info = graphene.List(TutorialType)
    all_translation_info = graphene.List(TransType, translation=graphene.NonNull(graphene.String))

    tutorial = graphene.Field(TutorialType, url=graphene.String(), id=graphene.String())
    graph = graphene.Field(GraphType, url=graphene.String(), id=graphene.String())

    @login_required
    def resolve_user_info(self, info: ResolveInfo, **kwargs):
        return info.context.user

    def resolve_all_categories(self, info: ResolveInfo, **kwargs):
        return Category.objects.all()

    def resolve_all_tutorial_info(self, info: ResolveInfo, **kwargs):
        return Tutorial.objects.all()

    def resolve_all_translation_info(self, info: ResolveInfo, **kwargs):
        translation = kwargs.get('translation', None)
        if translation:
            trans_table = get_translation_table(translation)
            if trans_table:
                return trans_table.objects.all()

            return None

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
