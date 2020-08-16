from typing import Type, Optional, Mapping, List

import graphene
from django.db.models import QuerySet, Model
from graphene_django import DjangoListField
from graphql import GraphQLError
from graphql import ResolveInfo

from .decorators import login_required, write_required, admin_required
from .filter_helpers import category_id_filter, tutorial_content_search, get_search_text, get_category_ids, \
    graph_content_search
from ..model.MetaModel import InvitationCode
from ..model.TutorialRelatedModel import GraphPriority, Uploads
from ..model.filters import show_published_only
from ..model.translation_collection import translation_tables
from ..models import Category, Tutorial, Graph, ExecResultJson, User, ROLES

from .types import UserType, CategoryType, TutorialType, GraphType, Code, ExecResultJsonType, CodeType, \
    GraphPriorityType, UploadsType, FilterContentType


def get_or_none(model: Type[Model], **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


class Query(graphene.ObjectType):
    # username_exist = graphene.Boolean(username=graphene.String(required=True))
    # email_exist = graphene.Boolean()
    user_info = graphene.Field(UserType)
    all_categories = DjangoListField(CategoryType)
    all_tutorial_info = DjangoListField(TutorialType, filter_content=FilterContentType())
    all_tutorial_info_no_code = DjangoListField(TutorialType, code=graphene.UUID())
    all_graph_info = DjangoListField(GraphType, filter_content=FilterContentType())
    all_code = DjangoListField(CodeType)
    all_exec_result = DjangoListField(ExecResultJsonType)
    all_supported_lang = graphene.List(graphene.String)
    all_graph_priority = graphene.List(GraphPriorityType)
    all_authors = DjangoListField(UserType)

    all_uploads = DjangoListField(UploadsType)

    category = graphene.Field(CategoryType, id=graphene.String(required=True))
    tutorial = graphene.Field(TutorialType,
                              url=graphene.String(),
                              id=graphene.String())
    graph = graphene.Field(GraphType,
                           url=graphene.String(),
                           id=graphene.String())
    code = graphene.Field(CodeType, id=graphene.UUID(required=True))
    invitation_codes = graphene.JSONString(required=True)

    # The most efficient method of finding whether a model with a unique field is a member of a QuerySet
    # def resolve_username_exist(self, info, username):
    #     return User.objects.filter(username=username).exists()

    # def resolve_email_exist(self, info, email):
    #     return User.objects.filter(email=email).exists()

    @login_required
    def resolve_user_info(self, info: ResolveInfo):
        return info.context.user

    @graphene.resolve_only_args
    def resolve_all_categories(self):
        return Category.objects.all()

    @staticmethod
    def tutorial_info_filter_helper(raw_queryset: QuerySet, filter_content: Optional[Mapping]) -> QuerySet:
        search_text: Optional[str] = get_search_text(filter_content)
        category_ids: Optional[List[str]] = get_category_ids(filter_content)

        final_queryset: QuerySet = category_id_filter(raw_queryset, category_ids=category_ids)
        final_queryset = tutorial_content_search(final_queryset, search_text=search_text)

        return final_queryset

    @graphene.resolve_only_args
    def resolve_all_tutorial_info(self, filter_content: Optional[Mapping] = None):
        raw_queryset = Tutorial.objects.all()
        if filter_content:
            return Query.tutorial_info_filter_helper(raw_queryset, filter_content)
        else:
            return raw_queryset

    @write_required
    @graphene.resolve_only_args
    def resolve_all_tutorial_info_no_code(self, code: str = None):
        if code:
            return Tutorial.objects.filter(code__isnull=True) | Tutorial.objects.filter(code__id=code)

        return Tutorial.objects.filter(code__isnull=True)

    @staticmethod
    def graph_info_filter_helper(raw_queryset: QuerySet, filter_content: Mapping) -> QuerySet:
        search_text: Optional[str] = get_search_text(filter_content)
        category_ids: Optional[List[str]] = get_category_ids(filter_content)

        final_queryset: QuerySet = category_id_filter(raw_queryset, category_ids=category_ids)
        final_queryset: QuerySet = graph_content_search(final_queryset, search_text=search_text)

        return final_queryset

    @graphene.resolve_only_args
    def resolve_all_graph_info(self, filter_content: Optional[Mapping] = None):
        raw_queryset = Graph.objects.all()
        if filter_content:
            return Query.graph_info_filter_helper(raw_queryset, filter_content)
        else:
            return raw_queryset

    @login_required
    @graphene.resolve_only_args
    def resolve_all_code(self):
        return Code.objects.all()

    @login_required
    @graphene.resolve_only_args
    def resolve_all_exec_result(self):
        return ExecResultJson.objects.all()

    @write_required
    @graphene.resolve_only_args
    def resolve_all_supported_lang(self):
        return translation_tables

    @write_required
    @graphene.resolve_only_args
    def resolve_all_graph_priority(self):
        return [GraphPriorityType(priority=priority, label=label) for priority, label in GraphPriority.choices]

    @write_required
    @graphene.resolve_only_args
    def resolve_all_authors(self):
        return User.objects.filter(role__gte=ROLES.TRANSLATOR)

    @write_required
    @graphene.resolve_only_args
    def resolve_all_uploads(self):
        return Uploads.objects.all()

    @write_required
    @graphene.resolve_only_args
    def resolve_category(self, id):
        return get_or_none(Category, id=id)

    @show_published_only
    @graphene.resolve_only_args
    def resolve_tutorial(self, is_published_only: bool, url=None, id=None):
        raw_result: QuerySet = Tutorial.objects.is_published_only_all(is_published_only=is_published_only)

        try:
            if url:
                return raw_result.get(url=url)
            elif id:
                return raw_result.get(id=id)
        except Tutorial.DoesNotExist:
            raise GraphQLError('The tutorial you requested with url=%s, id=%s does not exist.' % (url, id))

        raise GraphQLError('In tutorial query, the url and id arguments can not both be empty.')

    @show_published_only
    @graphene.resolve_only_args
    def resolve_graph(self, is_published_only: bool, url=None, id=None):
        raw_result: QuerySet = Graph.objects.is_published_only_all(is_published_only=is_published_only)

        if url:
            return raw_result.get(url=url)
        elif id:
            return raw_result.get(id=id)
        raise GraphQLError('The graph you requested with url=%s, id=%s does not exist.' % (url, id))

    @write_required
    @graphene.resolve_only_args
    def resolve_code(self, id: str):
        return Code.objects.get(id=id)

    @admin_required
    @graphene.resolve_only_args
    def resolve_invitation_codes(self):
        return InvitationCode.code_collection
