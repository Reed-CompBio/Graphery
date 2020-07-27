import graphene
from graphql import GraphQLError

from backend.graphql.decorators import write_required
from backend.intel_wrappers.intel_wrapper import CategoryWrapper, finalize_prerequisite_wrapper
from backend.model.TutorialRelatedModel import FAKE_UUID


class UpdateCategory(graphene.Mutation):
    class Arguments:
        pk = graphene.String(required=True)
        category = graphene.String(required=True)
        is_published = graphene.Boolean()

    success = graphene.Boolean(required=True)
    id = graphene.String(required=True)

    @write_required
    def mutate(self, info, category: str, pk: str = FAKE_UUID, is_published: bool = False):
        category_wrapper = CategoryWrapper().set_variables(id=pk,  category=category.strip(), is_published=is_published)
        finalize_prerequisite_wrapper(category_wrapper, overwrite=True)

        if category_wrapper.model is None:
            raise GraphQLError('Internal Error: cannot create model at this time!')

        return UpdateCategory(success=True, id=category_wrapper.model.id)
