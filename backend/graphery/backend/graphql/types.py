from ..model.mixins import time_date_mixin_field, published_mixin_field
from ..models import User
from ..models import Category, Tutorial, Graph, TutorialCode, ExecResultJson
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'is_verified', 'date_joined',
                  )


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('category',)


class TutorialType(DjangoObjectType):
    class Meta:
        model = Tutorial
        fields = ('id', 'url', 'authors',
                  'categories', 'abstract',
                  'content_md', 'content_html',
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
    class Meta:
        model = TutorialCode
        fields = ('tutorial', 'code', 'is_published') + \
                 time_date_mixin_field + \
                 published_mixin_field


class ExecResultJsonType(DjangoObjectType):
    class Meta:
        model = ExecResultJson
        fields = ('code', 'graph', 'json',
                  'is_published',
                  ) + \
                 time_date_mixin_field + \
                 published_mixin_field
