from typing import Tuple, Any, Iterable

from django.db.models import QuerySet
from graphene_django import DjangoListField
from graphql import ResolveInfo

from ..intel_wrappers.intel_wrapper import CategoryWrapper, TutorialAnchorWrapper, GraphWrapper, CodeWrapper, \
    ExecResultJsonWrapper, ENUSGraphContentWrapper, ZHCNTutorialContentWrapper, ENUSTutorialContentWrapper, \
    ZHCNGraphContentWrapper, UploadsWrapper
from ..model.TutorialRelatedModel import FAKE_UUID, GraphPriority, Uploads
from ..model.UserModel import ROLES
from ..model.filters import show_published_only
from ..model.mixins import field_adder, time_date_mixin_field, published_mixin_field, uuid_mixin_field
from ..model.translation_collection import add_trans_type
from ..model.MetaModel import InvitationCode
from ..models import User
from ..models import Category, Tutorial, Graph, Code, ExecResultJson
from ..models import ENUS, ZHCN, ENUSGraphContent, ZHCNGraphContent
from graphene_django.types import DjangoObjectType

import graphene

from copy import copy


InvitationCode.refresh_all_code()


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

    @graphene.resolve_only_args
    def resolve_role(self):
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
    authors = DjangoListField(UserType)
    abstract = graphene.String()
    content_md = graphene.String()
    content_html = graphene.String()
    is_published = graphene.Boolean()
    created_time = graphene.DateTime()
    modified_time = graphene.DateTime()

    @graphene.resolve_only_args
    def resolve_authors(self):
        return self.authors.all()


class RankType(graphene.ObjectType):
    level = graphene.Int(required=True)
    section = graphene.Int(required=True)


class RankInputType(graphene.InputObjectType):
    level = graphene.Argument(graphene.Int, required=True)
    section = graphene.Argument(graphene.Int, required=True)


class TutorialContentInputType(graphene.InputObjectType):
    id = graphene.UUID(required=True)
    title = graphene.String(required=True)
    tutorial_anchor = graphene.UUID(required=True)
    authors = graphene.List(graphene.UUID, required=True)
    abstract = graphene.String(required=True)
    content_md = graphene.String(required=True)
    content_html = graphene.String(required=True)
    is_published = graphene.Boolean(required=True)


class CategoryType(PublishedFilterBase, DjangoObjectType):
    @field_adder(uuid_mixin_field, published_mixin_field)
    class Meta:
        model = Category
        fields = ('category', 'tutorial_set')
        description = 'Category of a tutorial'


class TutorialType(PublishedFilterBase, DjangoObjectType):
    content = graphene.Field(TutorialInterface, translation=graphene.String(), default=graphene.String(), required=True)
    categories = DjangoListField(CategoryType, required=True)
    rank = graphene.Field(RankType, required=True)

    @show_published_only
    @graphene.resolve_only_args
    def resolve_categories(self, is_published_only: bool):
        raw_results = self.categories.is_published_only_all(is_published_only=is_published_only)
        return raw_results

    @show_published_only
    @graphene.resolve_only_args
    def resolve_content(self,
                        is_published_only: bool,
                        translation: str = 'en-us',
                        default: str = ''):
        return self.get_translation(translation, default, is_published_only)

    @show_published_only
    @graphene.resolve_only_args
    def resolve_code(self, is_published_only: bool):
        # TODO write a custom manager for this
        code = getattr(self, 'code', None)
        if code and (code.is_published or not is_published_only):
            return code
        return Code(id=FAKE_UUID, code='# Empty \n', tutorial=Tutorial())

    @graphene.resolve_only_args
    def resolve_rank(self):
        return RankType(level=self.level, section=self.section)

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
    abstract_md = graphene.String()
    abstract = graphene.String()
    is_published = graphene.Boolean()


class GraphContentInputType(graphene.InputObjectType):
    id = graphene.UUID(required=True)
    title = graphene.String(required=True)
    abstract_md = graphene.String(required=True)
    abstract = graphene.String(required=True)
    is_published = graphene.Boolean(required=True)
    graph_anchor = graphene.UUID(required=True)


class GraphPriorityType(graphene.ObjectType):
    priority = graphene.Int(required=True)
    label = graphene.String(required=True)


class GraphType(PublishedFilterBase, DjangoObjectType):
    priority = graphene.Field(GraphPriorityType, required=True)
    authors = DjangoListField(UserType)
    categories = DjangoListField(CategoryType)
    content = graphene.Field(GraphContentInterface,
                             translation=graphene.String(),
                             default=graphene.String(),
                             required=True)

    # Don't worried about tutorials and execresultjson_set since
    # they are convered under ManyToOneRel/ManyToManyRel/ManyToManyField
    # and will be automatically translated to DjangoListField

    @graphene.resolve_only_args
    def resolve_priority(self):
        return GraphPriorityType(priority=self.priority, label=GraphPriority(self.priority).label)

    @graphene.resolve_only_args
    def resolve_authors(self):
        return self.authors.all()

    @show_published_only
    @graphene.resolve_only_args
    def resolve_categories(self, is_published_only: bool):
        raw_results = self.categories.is_published_only_all(is_published_only=is_published_only)
        return raw_results

    @show_published_only
    @graphene.resolve_only_args
    def resolve_content(self,
                        is_published_only: bool,
                        translation: str = 'en-us',
                        default: str = ''):
        return self.get_translation(translation, default, is_published_only)

    @field_adder(time_date_mixin_field, published_mixin_field, uuid_mixin_field)
    class Meta:
        model = Graph
        fields = ('url', 'name', 'cyjs', 'categories',
                  'tutorials', 'execresultjson_set',
                  'priority')
        description = 'Graph type that contains info of a graph like ' \
                      'cyjs, style json, and layout json'


# the is_published fields below are not resolved with specific resolvers since
# they can't be accessed by API and the related fields are already covered
# under DjangoListField.


class CodeType(PublishedFilterBase, DjangoObjectType):
    is_published = graphene.Boolean()

    @graphene.resolve_only_args
    def resolve_is_published(self):
        return self.is_published

    @field_adder(time_date_mixin_field, published_mixin_field, uuid_mixin_field)
    class Meta:
        model = Code
        fields = ('tutorial', 'code', 'execresultjson_set')
        description = 'The code content of a tutorial. '


class ExecResultJsonType(DjangoObjectType):
    # TODO django can't query a user-defined property
    is_published = graphene.Boolean()

    @graphene.resolve_only_args
    def resolve_is_published(self):
        return self.is_published

    @field_adder(time_date_mixin_field, published_mixin_field, uuid_mixin_field)
    class Meta:
        model = ExecResultJson
        fields = ('code', 'graph', 'json',)
        description = 'The execution result of a piece of code on ' \
                      'a graph. '


class UploadsType(PublishedFilterBase, DjangoObjectType):
    relative_url = graphene.String()

    @graphene.resolve_only_args
    def resolve_url(self):
        return self.relative_url

    @field_adder(published_mixin_field, uuid_mixin_field)
    class Meta:
        model = Uploads
        fields = ('file', 'alias', 'relative_url')
        description = 'Uploaded files'


class DeletionEnum(graphene.Enum):
    CATEGORY = CategoryWrapper
    TUTORIAL_ANCHOR = TutorialAnchorWrapper
    GRAPH_ANCHOR = GraphWrapper
    CODE = CodeWrapper
    EXEC_RESULT_JSON = ExecResultJsonWrapper
    UPLOADS = UploadsWrapper
    ENUS_TUTORIAL_CONTENT = ENUSTutorialContentWrapper
    ZHCN_TUTORIAL_CONTENT = ZHCNTutorialContentWrapper
    ENUS_GRAPH_CONTENT = ENUSGraphContentWrapper
    ZHCN_GRAPH_CONTENT = ZHCNGraphContentWrapper


class FilterContentType(graphene.InputObjectType):
    search_text = graphene.String()
    category_ids = graphene.List(graphene.String)


TutorialTransBaseFields = ('tutorial_anchor', 'authors',
                           'abstract', 'content_md', 'content_html', )


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


GraphTransBaseFields = ('title', 'abstract_md', 'abstract')


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
