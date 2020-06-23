from typing import Tuple, Any, Iterable

from django.db.models import QuerySet
from graphql import GraphQLError

from ..model.mixins import uuid_field_adder, time_date_field_adder, published_field_adder
from ..model.translation_collection import add_trans_type, process_trans_name
from ..models import User
from ..models import Category, Tutorial, Graph, Code, ExecResultJson
from ..models import ENUS, ZHCN
from graphene_django.types import DjangoObjectType

import graphene

from copy import copy


# class HasPublishedDjangoObjectType(DjangoObjectType):
#     class Meta:
#         abstract = True
# 
#     @classmethod
#     def get_queryset(cls, queryset: QuerySet, info):
#         if info.context.user.is_anonymous:
#             return queryset.filter(published=True)
#         return queryset


class UserType(DjangoObjectType):
    role = graphene.Int(required=True)

    @uuid_field_adder
    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'is_verified', 'date_joined',
                  )
        description = 'User type. Login required to get info an account. '


class TutorialInterface(graphene.Interface):
    id = graphene.UUID()
    title = graphene.String()
    authors = graphene.List(graphene.String)
    abstract = graphene.String()
    content_md = graphene.String()
    content_html = graphene.String()
    is_published = graphene.Boolean()
    createdTime = graphene.DateTime()
    modifiedTime = graphene.DateTime()

    def resolve_authors(self, info, **kwargs):
        return self.authors.all().values_list('username', flat=True)


class CategoryType(DjangoObjectType):
    @published_field_adder
    class Meta:
        model = Category
        fields = ('category', 'tutorial_set')
        description = 'Category of a tutorial'


class TutorialType(DjangoObjectType):
    categories = graphene.List(graphene.String)
    content = graphene.Field(TutorialInterface, translation=graphene.String(), default=graphene.String(), required=True)

    def resolve_categories(self, info):
        return self.categories.all().values_list('category', flat=True)

    def resolve_content(self, info, translation: str = 'en-us', default: str = '', **kwargs):
        content = self.get_translation(translation, default)
        if content:
            return content
        raise GraphQLError(f'This tutorial does not provide {translation} translation for now. ' +
                           f'{f"No results come from {default} translation either" if default else ""}')

    def resolve_code(self, info):
        return getattr(self, 'code', Code(id='00000000-0000-0000-0000-000000000000', code='# Empty \n'))

    @classmethod
    def get_queryset(cls, queryset: QuerySet, info):
        if info.context.user.is_anonymous:
            return queryset.filter(published=True)
        return queryset

    @time_date_field_adder
    @published_field_adder
    @uuid_field_adder
    class Meta:
        model = Tutorial
        fields = ('url', 'content',
                  'categories', 'graph_set',
                  'code',
                  )

        description = 'The tutorial anchor for an tutorial article. ' \
                      'The contents are in translation table that ' \
                      'corresponds to certain language you want to ' \
                      'query. This type only contains meta info' \
                      'like id, url, category, associated graphs' \
                      'associated codes etc.'


class GraphType(DjangoObjectType):
    priority = graphene.Int(required=True)

    @time_date_field_adder
    @published_field_adder
    @uuid_field_adder
    class Meta:
        model = Graph
        fields = ('url', 'graph_info',
                  'cyjs', 'tutorials',
                  'execresultjson_set',
                  'priority'
                  )
        description = 'Graph type that contains info of a graph like ' \
                      'cyjs, style json, and layout json'


class CodeType(DjangoObjectType):
    is_published = graphene.Boolean()

    @time_date_field_adder
    @published_field_adder
    @uuid_field_adder
    class Meta:
        model = Code
        fields = ('tutorial', 'code', 'execresultjson_set')
        description = 'The code content of a tutorial. '


class ExecResultJsonType(DjangoObjectType):
    is_published = graphene.Boolean()

    @time_date_field_adder
    @published_field_adder
    @uuid_field_adder
    class Meta:
        model = ExecResultJson
        fields = ('code', 'graph', 'json', )
        description = 'The execution result of a piece of code on ' \
                      'a graph. '


TransBaseFields = ('tutorial_anchor', 'authors',
                   'abstract', 'content_md', 'content_html',
                   )


@time_date_field_adder
@published_field_adder
@uuid_field_adder
class MetaBase:
    interfaces = (TutorialInterface,)
    fields = TransBaseFields


def model_class_constructor(attributes: Iterable[Tuple[str, Any]]):
    meta_cls = copy(MetaBase)
    for attribute in attributes:
        setattr(meta_cls, attribute[0], attribute[1])
    return meta_cls


@add_trans_type
class ENUSTransType(DjangoObjectType):
    Meta = model_class_constructor((
        ('model', ENUS),
        ('description', 'The en-us translations of tutorials')
    ))


@add_trans_type
class ZHCNTransType(DjangoObjectType):
    Meta = model_class_constructor((
        ('model', ZHCN),
        ('description', 'The zh-cn translations of tutorials')
    ))
