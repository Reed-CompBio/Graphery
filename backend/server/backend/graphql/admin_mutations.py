from typing import List, Sequence, Type, Iterable, TypeVar

import graphene
from graphql import GraphQLError

from backend.graphql.decorators import write_required
from backend.graphql.types import CategoryType, TutorialType, GraphType
from backend.intel_wrappers.intel_wrapper import CategoryWrapper, finalize_prerequisite_wrapper, \
    TutorialAnchorWrapper, UserWrapper, GraphWrapper
from backend.model.TutorialRelatedModel import GraphPriority


T = TypeVar('T')


def process_model_wrapper(model_wrapper_class: Type[T], **kwargs) -> T:
    # noinspection PyArgumentList
    wrapper_instance = model_wrapper_class().set_variables(**kwargs)
    finalize_prerequisite_wrapper(wrapper_instance, overwrite=True)
    if wrapper_instance.model is None:
        raise GraphQLError('Internal Error: Cannot create model at this time.')

    return wrapper_instance


S = TypeVar('S')


def get_wrappers_by_ids(model_wrapper_class: Type[S],
                        model_info: Iterable[str]) -> List[S]:

    # noinspection PyArgumentList
    wrapper_collection = [model_wrapper_class().load_model(model_wrapper_class.model_class.objects.get(id=the_info))
                          for the_info in model_info]
    return wrapper_collection


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
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
        id = graphene.String(required=True)
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
        id = graphene.String(required=True)
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
    def mutate(self, info, id: str, url: str, name: str, cyjs: str, is_published: bool = False,
               priority: int = GraphPriority.TRIV, authors: Sequence[str] = (), categories: Sequence[str] = (),
               tutorials: Sequence[str] = ()):
        url = url.strip()
        name = name.strip()
        cyjs = cyjs.strip()

        author_wrappers: List[UserWrapper] = get_wrappers_by_ids(UserWrapper, authors)
        category_wrappers: List[CategoryWrapper] = get_wrappers_by_ids(CategoryWrapper, categories)
        tutorial_wrappers: List[TutorialAnchorWrapper] = get_wrappers_by_ids(TutorialAnchorWrapper, tutorials)

        graph_wrapper: GraphWrapper = process_model_wrapper(GraphWrapper,
                                                            id=id, url=url, name=name, cyjs=cyjs,
                                                            is_published=is_published, priority=priority,
                                                            authors=author_wrappers, categories=category_wrappers,
                                                            tutorials=tutorial_wrappers)

        return UpdateGraph(success=True, model=graph_wrapper.model)
