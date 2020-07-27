from typing import List, Sequence

import graphene
from graphql import GraphQLError

from backend.graphql.decorators import write_required
from backend.graphql.types import CategoryType
from backend.intel_wrappers.intel_wrapper import CategoryWrapper, finalize_prerequisite_wrapper, TutorialAnchorWrapper
from backend.model.TutorialRelatedModel import FAKE_UUID, Category


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        category = graphene.String(required=True)
        is_published = graphene.Boolean()

    success = graphene.Boolean(required=True)
    category = graphene.Field(CategoryType, required=True)

    @write_required
    def mutate(self, info, id: str, category: str, is_published: bool = False):
        category_wrapper = CategoryWrapper().set_variables(id=id,  category=category.strip(), is_published=is_published)
        finalize_prerequisite_wrapper(category_wrapper, overwrite=True)

        if category_wrapper.model is None:
            raise GraphQLError('Internal Error: cannot create model at this time!')

        return UpdateCategory(success=True, category=category_wrapper.model)


class UpdateTutorialAnchor(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        url = graphene.String(required=True)
        name = graphene.String(required=True)
        categories = graphene.List(graphene.String)
        is_published = graphene.Boolean()

    success = graphene.Boolean(required=True)

    @write_required
    def mutate(self, info, id: str, url: str, name: str, categories: Sequence[str] = (), is_published: bool = False):
        if len(categories) == 0:
            categories: Sequence[str] = ('uncategorized', )

        url = url.strip()
        name = name.strip()

        categories: List[CategoryWrapper] = [CategoryWrapper().load_model(Category.objects.get(category=cat))
                                             for cat in categories]

        tutorial_anchor_wrapper = TutorialAnchorWrapper().set_variables(id=id, url=url, name=name,
                                                                        categories=categories,
                                                                        is_published=is_published)

        finalize_prerequisite_wrapper(tutorial_anchor_wrapper, overwrite=True)

        return UpdateTutorialAnchor(success=True)

