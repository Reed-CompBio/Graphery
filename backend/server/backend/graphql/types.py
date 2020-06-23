from typing import Tuple, Any, Iterable

from django.db.models import QuerySet
from graphql import GraphQLError, ResolveInfo

from ..model.UserModel import ROLES
from ..model.mixins import uuid_field_adder, time_date_field_adder, published_field_adder
from ..model.translation_collection import add_trans_type, process_trans_name
from ..models import User
from ..models import Category, Tutorial, Graph, Code, ExecResultJson
from ..models import ENUS, ZHCN
from graphene_django.types import DjangoObjectType

import graphene

from copy import copy


class PublishedFilterBase(DjangoObjectType):
    class Meta:
        abstract = True

    @classmethod
    def get_queryset(cls, queryset: QuerySet, info: ResolveInfo):
        user = info.context.user
        if user.is_anonymous or user.role < ROLES.TRANSLATOR:
            return queryset.filter(is_published=True)
        return queryset


# TODO add fields explicitly using DjangoList, not graphene.List so that field works with get_queryset
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


class CategoryType(PublishedFilterBase, DjangoObjectType):
    @published_field_adder
    class Meta:
        model = Category
        fields = ('category', 'tutorial_set')
        description = 'Category of a tutorial'


class TutorialType(PublishedFilterBase, DjangoObjectType):
    content = graphene.Field(TutorialInterface, translation=graphene.String(), default=graphene.String(), required=True)
    categories = graphene.List(graphene.String)

    def resolve_categories(self, info):
        raw_results = self.categories.all()
        if info.context.user.is_anonymous or info.context.user.role < ROLES.TRANSLATOR:
            raw_results = raw_results.filter(is_published=True)
        return raw_results.values_list('category', flat=True)

    def resolve_content(self, info, translation: str = 'en-us', default: str = 'en-us', **kwargs):
        content = self.get_translation(translation, default)
        if content:
            if content.is_published or \
                    not (info.context.user.is_anonymous or info.context.user.role < ROLES.TRANSLATOR):
                return content
        raise GraphQLError(f'This tutorial does not provide {translation} translation for now. ' +
                           f'{f"No results come from {default} translation either" if default else ""}')

    def resolve_code(self, info):
        code = getattr(self, 'code', None)
        if code and \
                (code.is_published or not (
                        info.context.user.is_anonymous or info.context.user.role < ROLES.TRANSLATOR)):
            return code
        return Code(id='00000000-0000-0000-0000-000000000000', code='# Empty \n', tutorial=Tutorial())

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


class GraphType(PublishedFilterBase, DjangoObjectType):
    priority = graphene.Int(required=True)

    # Don't worried about tutorials and execresultjson_set since
    # they are convered under ManyToOneRel/ManyToManyRel/ManyToManyField
    # and will be automatically translated to DjangoListField

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


class CodeType(PublishedFilterBase, DjangoObjectType):
    is_published = graphene.Boolean()

    def resolve_is_published(self, info):
        return self.is_published

    @time_date_field_adder
    @published_field_adder
    @uuid_field_adder
    class Meta:
        model = Code
        fields = ('tutorial', 'code', 'execresultjson_set')
        description = 'The code content of a tutorial. '


class ExecResultJsonType(PublishedFilterBase, DjangoObjectType):
    is_published = graphene.Boolean()

    def resolve_is_published(self, info):
        return self.is_published

    @time_date_field_adder
    @published_field_adder
    @uuid_field_adder
    class Meta:
        model = ExecResultJson
        fields = ('code', 'graph', 'json',)
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
class ENUSTransType(PublishedFilterBase, DjangoObjectType):
    Meta = model_class_constructor((
        ('model', ENUS),
        ('description', 'The en-us translations of tutorials')
    ))


@add_trans_type
class ZHCNTransType(PublishedFilterBase, DjangoObjectType):
    Meta = model_class_constructor((
        ('model', ZHCN),
        ('description', 'The zh-cn translations of tutorials')
    ))
