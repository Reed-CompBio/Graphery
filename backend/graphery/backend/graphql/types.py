from ..model.mixins import time_date_mixin_field, published_mixin_field
from ..models import User
from ..models import Category, Tutorial, Graph, TutorialCode, ExecResultJson
from ..models import ENUS, ZHCN
from graphene_django.types import DjangoObjectType
import graphene


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'is_verified', 'date_joined',
                  )


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('category', 'tutorial_set')


class TutorialType(DjangoObjectType):
    class Meta:
        model = Tutorial
        fields = ('id', 'url',
                  'categories', 'graph_set',
                  'tutorialcode_set',
                  ) + \
                 time_date_mixin_field + \
                 published_mixin_field


class GraphType(DjangoObjectType):
    class Meta:
        model = Graph
        fields = ('id', 'url', 'graph_info',
                  'initial_cyjs', 'layouts',
                  'styles', 'tutorial'
                  ) + \
                 time_date_mixin_field + \
                 published_mixin_field


class TutorialCodeType(DjangoObjectType):
    is_published = graphene.Boolean()

    class Meta:
        model = TutorialCode
        fields = ('tutorial', 'code', 'is_published') + \
                 time_date_mixin_field + \
                 published_mixin_field


class ExecResultJsonType(DjangoObjectType):
    is_published = graphene.Boolean()

    class Meta:
        model = ExecResultJson
        fields = ('code', 'graph', 'json',
                  'is_published',
                  ) + \
                 time_date_mixin_field + \
                 published_mixin_field


TransBaseFields = ('original_tutorial', 'author',
                   'abstract', 'content_md', 'content_html',
                   ) + \
                  time_date_mixin_field + \
                  published_mixin_field


class TutorialInterface(graphene.Interface):
    authors = graphene.List(UserType)
    original_tutorial = graphene.Field(TutorialType)
    abstract = graphene.String()
    content_md = graphene.String()
    content_html = graphene.String()


class ENUSTransType(DjangoObjectType):
    class Meta:
        interfaces = (TutorialInterface,)
        model = ENUS
        fields = TransBaseFields


class ZHCNTransType(DjangoObjectType):
    class Meta:
        interfaces = (TutorialInterface,)
        model = ZHCN
        fields = TransBaseFields
