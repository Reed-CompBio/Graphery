from typing import List, Sequence, Type

import graphene
from graphql import GraphQLError

from backend.graphql.decorators import write_required
from backend.graphql.types import CategoryType, TutorialType
from backend.intel_wrappers.intel_wrapper import CategoryWrapper, finalize_prerequisite_wrapper, TutorialAnchorWrapper
from backend.intel_wrappers.wrapper_bases import AbstractWrapper
from backend.model.TutorialRelatedModel import Category


def process_model_wrapper(model_wrapper_class: Type[AbstractWrapper], **kwargs) -> AbstractWrapper:
    # noinspection PyArgumentList
    wrapper_instance = model_wrapper_class().set_variables(**kwargs)
    finalize_prerequisite_wrapper(wrapper_instance, overwrite=True)
    if wrapper_instance.model is None:
        raise GraphQLError('Internal Error: Cannot create model at this time.')

    return wrapper_instance


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        category = graphene.String(required=True)
        is_published = graphene.Boolean()

    success = graphene.Boolean(required=True)
    category = graphene.Field(CategoryType, required=True)

    @write_required
    def mutate(self, info, id: str, category: str, is_published: bool = False):
        category_wrapper = process_model_wrapper(CategoryWrapper,
                                                 id=id,  category=category.strip(), is_published=is_published)

        return UpdateCategory(success=True, category=category_wrapper.model)


class UpdateTutorialAnchor(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        url = graphene.String(required=True)
        name = graphene.String(required=True)
        categories = graphene.List(graphene.String)
        is_published = graphene.Boolean()

    success = graphene.Boolean(required=True)
    tutorial = graphene.Field(TutorialType, required=True)

    @write_required
    def mutate(self, info, id: str, url: str, name: str, categories: Sequence[str] = (), is_published: bool = False):
        if len(categories) == 0:
            categories: Sequence[str] = ('uncategorized', )

        url = url.strip()
        name = name.strip()

        categories: List[CategoryWrapper] = [CategoryWrapper().load_model(Category.objects.get(id=cat))
                                             for cat in categories]

        tutorial_anchor_wrapper = process_model_wrapper(TutorialAnchorWrapper,
                                                        id=id, url=url, name=name,
                                                        categories=categories,
                                                        is_published=is_published)

        return UpdateTutorialAnchor(success=True, tutorial=tutorial_anchor_wrapper.model)

