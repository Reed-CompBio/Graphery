from ..model.mixins import time_date_mixin_field, published_mixin_field
from ..models import User
from ..models import Category, Tutorial, Graph, TutorialCode, ExecResultJson
from ..models import ZHCN
from graphene_django.types import DjangoObjectType
import graphene


class TutorialInterface(graphene.Interface):
    abstract = graphene.String()
    content_md = graphene.String()
    content_html = graphene.String()


class UserType(DjangoObjectType):
    all_articles = graphene.List(TutorialInterface)
    original_articles = graphene.List(TutorialInterface)
    translated_articles = graphene.List(TutorialInterface)

    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'is_verified', 'date_joined',
                  'all_articles', 'original_articles',
                  'translated_articles'
                  )


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('category', 'tutorial_set')


class TutorialType(DjangoObjectType):
    class Meta:
        interfaces = (TutorialInterface, )
        model = Tutorial
        fields = ('id', 'url', 'authors',
                  'categories', 'abstract',
                  'content_md', 'content_html',
                  'graph_set', 'tutorialcode_set',
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


class TransInterface(graphene.Interface):
    translator = graphene.Field(UserType)
    original_tutorial = graphene.Field(TutorialType)


class TransType(graphene.ObjectType):
    class Meta:
        interfaces = (TutorialInterface, TransInterface, )


class ZHCNTransType(DjangoObjectType):
    class Meta:
        types = (TransType, )
        model = ZHCN
        fields = ('original_tutorial', 'translator',
                  'abstract', 'content_md', 'content_html',
                  ) + \
                 time_date_mixin_field + \
                 published_mixin_field



