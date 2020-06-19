import graphene
from graphql_jwt.decorators import login_required
from graphql.execution.base import ResolveInfo

from ..model.trans_list import get_translation_table
from ..models import User
from ..models import Category, Tutorial, Graph

from .types import UserType, CategoryType, TutorialType, GraphType, TutorialInterface


class Query(graphene.ObjectType):
    username_exist = graphene.Boolean(username=graphene.String(required=True))
    email_exist = graphene.Boolean()
    user_info = graphene.Field(UserType)
    all_categories = graphene.List(CategoryType)
    all_tutorial_info = graphene.List(TutorialType)
    all_translation_info = graphene.List(TutorialInterface,
                                         translation=graphene.String(default_value='en-us'))

    tutorial = graphene.Field(TutorialInterface,
                              url=graphene.String(default_value=None),
                              id=graphene.String(default_value=None),
                              translation=graphene.String(default_value='en-us'))
    graph = graphene.Field(GraphType,
                           url=graphene.String(default_value=None),
                           id=graphene.String(default_value=None))

    # The most efficient method of finding whether a model with a unique field is a member of a QuerySet
    def resolve_username_exist(self, info, username):
        return User.objects.filter(username=username).exists()

    def resolve_email_exist(self, info, email):
        return User.objects.filter(email=email).exists()

    @login_required
    def resolve_user_info(self, info: ResolveInfo, **kwargs):
        return info.context.user

    def resolve_all_categories(self, info: ResolveInfo, **kwargs):
        return Category.objects.all()

    def resolve_all_tutorial_info(self, info: ResolveInfo, **kwargs):
        return Tutorial.objects.all()

    def resolve_all_translation_info(self, info: ResolveInfo, **kwargs):
        trans_table = get_translation_table(kwargs['translation'])
        if trans_table:
            return trans_table.objects.all()

        return None

    def resolve_tutorial(self, info: ResolveInfo, **kwargs):
        url = kwargs['url']
        idt = kwargs['id']
        translation_table = get_translation_table(kwargs['translation'])
        if translation_table:
            if url:
                return translation_table.objects.get(original_tutorial__url=url)
            elif idt:
                return translation_table.objects.get(original_tutorial__id=idt)
        return None

    def resolve_graph(self, info: ResolveInfo, **kwargs):
        url = kwargs['url']
        idt = kwargs['id']
        if url:
            return Graph.objects.get(url=url)
        elif idt:
            return Graph.objects.get(id=idt)
        return None
