from typing import Tuple, Any, Iterable

from django.db.models import QuerySet
from graphql import ResolveInfo

from ..model.TutorialRelatedModel import FAKE_UUID, GraphPriority
from ..model.UserModel import ROLES
from ..model.filters import show_published_only
from ..model.mixins import field_adder, time_date_mixin_field, published_mixin_field, uuid_mixin_field
from ..model.translation_collection import add_trans_type
from ..models import User
from ..models import Category, Tutorial, Graph, Code, ExecResultJson
from ..models import ENUS, ZHCN, ENUSGraphContent, ZHCNGraphContent
from graphene_django.types import DjangoObjectType

import graphene

from copy import copy


class PublishedFilterBase(DjangoObjectType):
    class Meta:
        abstract = True

    @classmethod
    def get_queryset(cls, queryset: QuerySet, info: ResolveInfo):
        # use show_published decorator
        if info.context.user.is_anonymous or info.context.user.role < ROLES.TRANSLATOR:
            return queryset.filter(is_published=True)
        return queryset


# TODO add fields explicitly using DjangoList, not graphene.List so that field works with get_queryset
class UserType(DjangoObjectType):
    role = graphene.String(required=True)

    def resolve_role(self, info):
        return ROLES(self.role).label

    @field_adder(uuid_mixin_field)
    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'is_verified', 'date_joined',)
        description = 'User type. Login required to get info an account. '


class TutorialInterface(graphene.Interface):
    id = graphene.UUID()
    title = graphene.String()
    authors = graphene.List(graphene.String)
    abstract = graphene.String()
    content_md = graphene.String()
    content_html = graphene.String()
    is_published = graphene.Boolean()
    created_time = graphene.DateTime()
    modified_time = graphene.DateTime()

    def resolve_authors(self, info):
        return self.authors.all().values_list('username', flat=True)


class CategoryType(PublishedFilterBase, DjangoObjectType):
    @field_adder(uuid_mixin_field, published_mixin_field)
    class Meta:
        model = Category
        fields = ('category', 'tutorial_set')
        description = 'Category of a tutorial'


class TutorialType(PublishedFilterBase, DjangoObjectType):
    content = graphene.Field(TutorialInterface, translation=graphene.String(), default=graphene.String(), required=True)
    categories = graphene.List(graphene.String)

    @show_published_only
    def resolve_categories(self, info, is_published_only: bool):
        raw_results = self.categories.is_published_only_all(is_published_only=is_published_only)
        return raw_results.values_list('category', flat=True)

    @show_published_only
    def resolve_content(self,
                        info,
                        is_published_only: bool,
                        translation: str = 'en-us',
                        default: str = ''):
        return self.get_translation(translation, default, is_published_only)

    @show_published_only
    def resolve_code(self, info, is_published_only: bool):
        # TODO write a custom manager for this
        code = getattr(self, 'code', None)
        if code and (code.is_published or not is_published_only):
            return code
        return Code(id=FAKE_UUID, code='# Empty \n', tutorial=Tutorial())

    @field_adder(time_date_mixin_field, published_mixin_field, uuid_mixin_field)
    class Meta:
        model = Tutorial
        fields = ('url', 'name',
                  'content', 'categories',
                  'graph_set', 'code',)

        description = 'The tutorial anchor for an tutorial article. ' \
                      'The contents are in translation table that ' \
                      'corresponds to certain language you want to ' \
                      'query. This type only contains meta info' \
                      'like id, url, category, associated graphs' \
                      'associated codes etc.'


class GraphContentInterface(graphene.Interface):
    id = graphene.UUID()
    title = graphene.String()
    abstract = graphene.String()
    is_published = graphene.Boolean()


class GraphType(PublishedFilterBase, DjangoObjectType):
    priority = graphene.String(required=True)
    authors = graphene.List(graphene.String)
    content = graphene.Field(GraphContentInterface,
                             translation=graphene.String(),
                             default=graphene.String(),
                             required=True)

    # Don't worried about tutorials and execresultjson_set since
    # they are convered under ManyToOneRel/ManyToManyRel/ManyToManyField
    # and will be automatically translated to DjangoListField

    def resolve_priority(self, info):
        return GraphPriority(self.priority).label

    def resolve_authors(self, info):
        return self.authors.all().values_list('username', flat=True)

    @show_published_only
    def resolve_content(self,
                        info: ResolveInfo,
                        is_published_only: bool,
                        translation: str = 'en-us',
                        default: str = ''):
        return self.get_translation(translation, default, is_published_only)

    @field_adder(time_date_mixin_field, published_mixin_field, uuid_mixin_field)
    class Meta:
        model = Graph
        fields = ('url', 'name', 'cyjs',
                  'tutorials', 'execresultjson_set',
                  'priority')
        description = 'Graph type that contains info of a graph like ' \
                      'cyjs, style json, and layout json'


# the is_published fields below are not resolved with specific resolvers since
# they can't be accessed by API and the related fields are already covered
# under DjangoListField.


class CodeType(PublishedFilterBase, DjangoObjectType):
    is_published = graphene.Boolean()

    def resolve_is_published(self, info):
        return self.is_published

    @field_adder(time_date_mixin_field, published_mixin_field, uuid_mixin_field)
    class Meta:
        model = Code
        fields = ('tutorial', 'code', 'execresultjson_set')
        description = 'The code content of a tutorial. '


class ExecResultJsonType(DjangoObjectType):
    # TODO django can't query a user-defined property
    is_published = graphene.Boolean()

    def resolve_is_published(self, info):
        return self.is_published

    @field_adder(time_date_mixin_field, published_mixin_field, uuid_mixin_field)
    class Meta:
        model = ExecResultJson
        fields = ('code', 'graph', 'json',)
        description = 'The execution result of a piece of code on ' \
                      'a graph. '


TutorialTransBaseFields = ('tutorial_anchor', 'authors',
                           'abstract', 'content_md', 'content_html',
                           )


@field_adder(time_date_mixin_field, published_mixin_field, uuid_mixin_field)
class TutorialTransMetaBase:
    interfaces = (TutorialInterface,)
    fields = TutorialTransBaseFields


def model_class_constructor(base_meta: type, attributes: Iterable[Tuple[str, Any]]):
    meta_cls = copy(base_meta)
    for attribute in attributes:
        setattr(meta_cls, attribute[0], attribute[1])
    return meta_cls


@add_trans_type
class ENUSTransType(PublishedFilterBase, DjangoObjectType):
    Meta = model_class_constructor(TutorialTransMetaBase, (
        ('model', ENUS),
        ('description', 'The en-us translations of tutorials')
    ))


@add_trans_type
class ZHCNTransType(PublishedFilterBase, DjangoObjectType):
    Meta = model_class_constructor(TutorialTransMetaBase, (
        ('model', ZHCN),
        ('description', 'The zh-cn translations of tutorials')
    ))


GraphTransBaseFields = ('title', 'abstract')


@field_adder(time_date_mixin_field, published_mixin_field, uuid_mixin_field)
class GraphTransMetaBase:
    interfaces = (GraphContentInterface,)
    fields = GraphTransBaseFields


@add_trans_type
class ENUSGraphTransType(PublishedFilterBase, DjangoObjectType):
    Meta = model_class_constructor(GraphTransMetaBase, (
        ('model', ENUSGraphContent),
        ('description', 'The en-us translation of graphs')
    ))


@add_trans_type
class ZHCNGraphTransType(PublishedFilterBase, DjangoObjectType):
    Meta = model_class_constructor(GraphTransMetaBase, (
        ('model', ZHCNGraphContent),
        ('description', 'The zh-cn translation of graphs')
    ))
