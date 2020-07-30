from typing import List, Sequence, Mapping

import graphene
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphql import GraphQLError

from backend.graphql.decorators import write_required
from backend.graphql.types import CategoryType, TutorialType, GraphType, CodeType
from backend.graphql.utils import process_model_wrapper, get_wrappers_by_ids, get_wrapper_by_id
from backend.intel_wrappers.intel_wrapper import CategoryWrapper, \
    TutorialAnchorWrapper, UserWrapper, GraphWrapper, CodeWrapper
from backend.model.TutorialRelatedModel import GraphPriority


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        category = graphene.String(required=True)
        is_published = graphene.Boolean()

    success = graphene.Boolean(required=True)
    model = graphene.Field(CategoryType, required=True)

    @write_required
    def mutate(self, info, id: str, category: str, is_published: bool = False):
        category_wrapper = process_model_wrapper(CategoryWrapper,
                                                 id=id,  category=category.strip(), is_published=is_published)

        return UpdateCategory(success=True, model=category_wrapper.model)


class UpdateTutorialAnchor(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        url = graphene.String(required=True)
        name = graphene.String(required=True)
        categories = graphene.List(graphene.String)
        is_published = graphene.Boolean()

    success = graphene.Boolean(required=True)
    model = graphene.Field(TutorialType, required=True)

    @write_required
    def mutate(self, info, id: str, url: str, name: str, categories: Sequence[str] = (), is_published: bool = False):
        if len(categories) == 0:
            categories: Sequence[str] = ('uncategorized', )

        url = url.strip()
        name = name.strip()

        categories: List[CategoryWrapper] = get_wrappers_by_ids(CategoryWrapper, categories)

        tutorial_anchor_wrapper = process_model_wrapper(TutorialAnchorWrapper,
                                                        id=id, url=url, name=name,
                                                        categories=categories,
                                                        is_published=is_published)

        return UpdateTutorialAnchor(success=True, model=tutorial_anchor_wrapper.model)


class UpdateGraph(graphene.Mutation):
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

    success = graphene.Boolean()
    model = graphene.Field(GraphType)

    @write_required
    def mutate(self, info, id: str, url: str, name: str, cyjs: Mapping, is_published: bool = False,
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


class UpdateCode(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        code = graphene.String(required=True)
        tutorial = graphene.UUID(required=True)

    success = graphene.Boolean(required=True)
    model = graphene.Field(CodeType, required=True)

    @write_required
    def mutate(self, info, id: str, code: str, tutorial: str):
        tutorial_wrapper = get_wrapper_by_id(TutorialAnchorWrapper, tutorial)

        code_wrapper = process_model_wrapper(CodeWrapper,
                                             id=id, code=code, tutorial=tutorial_wrapper)

        return UpdateCode(success=True, model=code_wrapper.model)


class UpdateStatics(graphene.Mutation):
    success = graphene.Boolean(required=True)

    @write_required
    def mutate(self, info):
        files: Mapping[InMemoryUploadedFile] = info.context.FILES

        if len(files) == 0 or not all('image' in file.content_type for file in files.values()):
            raise GraphQLError('No files are added.')

        for upload_name, file in files.items():
            # do something
            pass

        return UpdateStatics(success=True)
