import json
from typing import List, Sequence, Mapping, Type, Optional, MutableMapping

import graphene
from django.db import transaction
from django.db.models import QuerySet
from graphene.types.generic import GenericScalar
from graphql import GraphQLError

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

from backend.graphql.decorators import write_required, admin_required
from backend.graphql.mutation_base import SuccessMutationBase
from backend.graphql.types import CategoryType, TutorialType, GraphType, CodeType, TutorialInterface, \
    TutorialContentInputType, GraphContentInputType, GraphContentInterface, ExecResultJsonType, DeletionEnum, \
    RankInputType, FailedMissionType
from backend.graphql.utils import process_model_wrapper, get_wrappers_by_ids, get_wrapper_by_id
from backend.intel_wrappers.intel_wrapper import CategoryWrapper, \
    TutorialAnchorWrapper, UserWrapper, GraphWrapper, CodeWrapper, TutorialTranslationContentWrapper, \
    GraphTranslationContentWrapper, ExecResultJsonWrapper, UploadsWrapper, _result_json_updater
from backend.intel_wrappers.wrapper_bases import AbstractWrapper
from backend.model.TranslationModels import TranslationBase, GraphTranslationBase
from backend.model.TutorialRelatedModel import GraphPriority, Graph
from backend.model.translation_collection import get_translation_table, get_graph_info_trans_table


class UpdateCategory(SuccessMutationBase):
    class Arguments:
        id = graphene.UUID(required=True)
        category = graphene.String(required=True)
        is_published = graphene.Boolean()

    model = graphene.Field(CategoryType, required=True)

    @write_required
    def mutate(self, _, id: str, category: str, is_published: bool = False):
        category_wrapper = process_model_wrapper(CategoryWrapper,
                                                 id=id, category=category.strip(), is_published=is_published)

        return UpdateCategory(success=True, model=category_wrapper.model)


class UpdateTutorialAnchor(SuccessMutationBase):
    class Arguments:
        id = graphene.UUID(required=True)
        url = graphene.String(required=True)
        name = graphene.String(required=True)
        rank = graphene.Argument(RankInputType, required=True)
        categories = graphene.List(graphene.String)
        is_published = graphene.Boolean()

    model = graphene.Field(TutorialType, required=True)

    @write_required
    def mutate(self, _, id: str, url: str, name: str, rank: Mapping, categories: Sequence[str] = (),
               is_published: bool = False):
        if len(categories) == 0:
            categories: Sequence[str] = \
                (CategoryWrapper.model_class.objects.get_or_create(category='uncategorized')[0].id,)

        url = url.strip()
        name = name.strip()

        categories: List[CategoryWrapper] = get_wrappers_by_ids(CategoryWrapper, categories)

        tutorial_anchor_wrapper = process_model_wrapper(TutorialAnchorWrapper,
                                                        id=id, url=url, name=name,
                                                        level=rank['level'], section=rank['section'],
                                                        categories=categories,
                                                        is_published=is_published)

        return UpdateTutorialAnchor(success=True, model=tutorial_anchor_wrapper.model)


class UpdateGraph(SuccessMutationBase):
    class Arguments:
        id = graphene.UUID(required=True)
        url = graphene.String(required=True)
        name = graphene.String(required=True)
        cyjs = graphene.JSONString(required=True)
        is_published = graphene.Boolean()
        priority = graphene.Int()
        authors = graphene.List(graphene.String)
        categories = graphene.List(graphene.String)
        tutorials = graphene.List(graphene.String)

    model = graphene.Field(GraphType, required=True)

    @write_required
    def mutate(self, _, id: str, url: str, name: str, cyjs: Mapping, is_published: bool = False,
               priority: int = GraphPriority.TRIV, authors: Sequence[str] = (), categories: Sequence[str] = (),
               tutorials: Sequence[str] = ()):
        url = url.strip()
        name = name.strip()

        if not isinstance(cyjs, Mapping):
            raise GraphQLError('CYJS must be a json mapping')

        author_wrappers: List[UserWrapper] = get_wrappers_by_ids(UserWrapper, authors)
        category_wrappers: List[CategoryWrapper] = get_wrappers_by_ids(CategoryWrapper, categories)
        tutorial_wrappers: List[TutorialAnchorWrapper] = get_wrappers_by_ids(TutorialAnchorWrapper, tutorials)

        graph_wrapper: GraphWrapper = process_model_wrapper(GraphWrapper,
                                                            id=id, url=url, name=name, cyjs=cyjs,
                                                            is_published=is_published, priority=priority,
                                                            authors=author_wrappers, categories=category_wrappers,
                                                            tutorials=tutorial_wrappers)

        return UpdateGraph(success=True, model=graph_wrapper.model)


class UpdateCode(SuccessMutationBase):
    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String(required=True)
        code = graphene.String(required=True)
        tutorial = graphene.UUID(required=True)

    model = graphene.Field(CodeType, required=True)

    @write_required
    def mutate(self, _, id: str, name: str, code: str, tutorial: str):
        tutorial_wrapper = get_wrapper_by_id(TutorialAnchorWrapper, tutorial)

        code_wrapper = process_model_wrapper(CodeWrapper,
                                             id=id, name=name, code=code, tutorial=tutorial_wrapper)

        return UpdateCode(success=True, model=code_wrapper.model)


class UploadStatic(SuccessMutationBase):
    urls = graphene.List(graphene.String, required=True)

    @write_required
    def mutate(self, info):

        files: Mapping[str, InMemoryUploadedFile] = info.context.FILES

        if len(files) == 0:
            raise GraphQLError('No files are added.')

        if not all('image' in file.content_type for file in files.values()):
            raise GraphQLError('Invalid form data.')

        wrappers: List[UploadsWrapper] = []

        for name, file in files.items():
            wrappers.append(process_model_wrapper(UploadsWrapper, file=file, alias=name))

        return UploadStatic(success=True, urls=[wrapper.model.relative_url for wrapper in wrappers])


class DeleteStatic(SuccessMutationBase):
    upload_url_prefix = f'/{settings.UPLOAD_STATICS_ENTRY}/'

    class Arguments:
        url = graphene.String(required=True)

    @write_required
    def mutate(self, _, url: str):
        raise DeprecationWarning


class UpdateTutorialContent(SuccessMutationBase):
    class Arguments:
        lang = graphene.String(required=True)
        content = TutorialContentInputType()

    model = graphene.Field(TutorialInterface, required=True)

    @write_required
    def mutate(self, _, lang: str, content: MutableMapping):
        translation_table: Optional[Type[TranslationBase]] = get_translation_table(lang.strip())

        if not translation_table:
            raise GraphQLError(f'Language {lang} is no supported.')

        content['authors'] = get_wrappers_by_ids(UserWrapper, content['authors'])
        content['tutorial_anchor'] = get_wrapper_by_id(TutorialAnchorWrapper, content['tutorial_anchor'])

        graph_set: QuerySet[Graph] = Graph.objects.filter(id__in=content.pop('graph_set'))

        with transaction.atomic():
            tutorial_content_wrapper = process_model_wrapper(TutorialTranslationContentWrapper,
                                                             model_class=translation_table, **content)

            tutorial_content_wrapper.model.tutorial_anchor.graph_set.set(graph_set)

            if hasattr(tutorial_content_wrapper.model, 'code'):
                code_list = [tutorial_content_wrapper.model.code]
                _result_json_updater(code_list, graph_set)

        return UpdateTutorialContent(success=True, model=tutorial_content_wrapper.model)


class UpdateGraphInfoContent(SuccessMutationBase):
    class Arguments:
        lang = graphene.String(required=True)
        content = GraphContentInputType()

    model = graphene.Field(GraphContentInterface, required=True)

    @write_required
    def mutate(self, _, lang: str, content: MutableMapping):
        graph_info_translation_table: Optional[Type[GraphTranslationBase]] = get_graph_info_trans_table(lang.strip())

        if not graph_info_translation_table:
            raise GraphQLError(f'Language {lang} is not supported.')

        content['graph_anchor'] = get_wrapper_by_id(GraphWrapper, content['graph_anchor'])

        graph_info_content_wrapper = process_model_wrapper(GraphTranslationContentWrapper,
                                                           model_class=graph_info_translation_table,
                                                           **content)

        return UpdateGraphInfoContent(success=True, model=graph_info_content_wrapper.model)


class UpdateResultJson(SuccessMutationBase):
    class Arguments:
        code_id = graphene.UUID(required=True)
        result_json_dict = GenericScalar(required=True)

    models = graphene.List(ExecResultJsonType, required=True)

    @write_required
    def mutate(self, _, code_id, result_json_dict: MutableMapping):
        if not isinstance(result_json_dict, Mapping):
            raise GraphQLError('`result_json_dict` must be a mapping of graph ids and result jsons')

        code_wrapper: CodeWrapper = get_wrapper_by_id(CodeWrapper, code_id)

        result_json_models = []
        for key, value in result_json_dict.items():
            graph_wrapper: GraphWrapper = get_wrapper_by_id(GraphWrapper, key)
            json_obj = json.loads(value) if isinstance(value, str) else value
            result_wrapper: ExecResultJsonWrapper = process_model_wrapper(ExecResultJsonWrapper,
                                                                          code=code_wrapper, graph=graph_wrapper,
                                                                          json=json_obj)
            result_json_models.append(result_wrapper.model)

        return UpdateResultJson(success=True, models=result_json_models)


class DeleteContent(SuccessMutationBase):
    class Arguments:
        content_type = graphene.Argument(DeletionEnum, required=True)
        id = graphene.Argument(graphene.UUID, required=True)

    @admin_required
    def mutate(self, info, content_type: Type[AbstractWrapper], id: str):
        wrapper = get_wrapper_by_id(content_type, id)
        wrapper.delete_model()

        return DeleteContent(success=True, )


class RefreshInvitationCode(SuccessMutationBase):
    invitation_codes = graphene.JSONString(required=True)

    @admin_required
    @graphene.resolve_only_args
    def mutate(self):
        raise DeprecationWarning('This API is deprecated.')


class ExecuteCode(SuccessMutationBase):
    class Arguments:
        code_ids = graphene.List(graphene.UUID)

    failed_missions = graphene.List(FailedMissionType, required=True)

    @admin_required
    @graphene.resolve_only_args
    def mutate(self, code_ids: Optional[List] = None):
        if code_ids is None:
            code_objects = CodeWrapper.model_class.objects.all()
        else:
            code_objects = CodeWrapper.model_class.objects.filter(id__in=code_ids)
        failed_missions = []

        for code in code_objects:
            code_graph = code.tutorial.graph_set.all()
            failed_missions.extend(_result_json_updater([code], code_graph))

        success = len(failed_missions) == 0
        return ExecuteCode(success=success, failed_missions=list(
            FailedMissionType(code=m[0], graph=m[1], error=str(m[2])) for m in failed_missions
        ))
