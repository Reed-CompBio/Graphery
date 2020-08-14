from typing import TypeVar, Type, List, Iterable

from django.db.models import QuerySet
from django.contrib.postgres.search import SearchVector
from graphql import GraphQLError

from backend.intel_wrappers.intel_wrapper import finalize_prerequisite_wrapper
from backend.model.translation_collection import translation_tables

T = TypeVar('T')


def process_model_wrapper(model_wrapper_class: Type[T], **kwargs) -> T:
    wrapper_instance = model_wrapper_class().set_variables(**kwargs)
    finalize_prerequisite_wrapper(wrapper_instance, overwrite=True)
    if wrapper_instance.model is None:
        raise GraphQLError('Internal Error: Cannot create model at this time.')

    return wrapper_instance


S = TypeVar('S')


def get_wrappers_by_ids(model_wrapper_class: Type[S],
                        model_info: Iterable[str]) -> List[S]:
    # noinspection PyArgumentList
    wrapper_collection = [get_wrapper_by_id(model_wrapper_class, the_info)
                          for the_info in model_info]
    return wrapper_collection


def get_wrapper_by_id(model_wrapper_class: Type[S], model_id: str) -> S:
    return model_wrapper_class().load_model(model_wrapper_class.model_class.objects.get(id=model_id))


def skip_none(func):
    def wrapper(*args, **kwargs):
        if any(value is None for value in kwargs.values()):
            return args[0]
        else:
            return func(*args, **kwargs)

    return wrapper


content_search_vector_parts = ['%s__title', '%s__abstract', '%s__content_md', ]
content_search_vector_attrs = ['url', 'name']


@skip_none
def tutorial_content_search(queryset: QuerySet, search_text: str) -> QuerySet:
    return queryset.annotate(
        search=SearchVector(*(part % trans_type
                              for trans_type in translation_tables
                              for part in content_search_vector_parts),
                            *(attr for attr in content_search_vector_attrs))
    ).filter(search=search_text)


@skip_none
def category_id_filter(queryset: QuerySet, category_ids: List[str]) -> QuerySet:
    for cat_id in category_ids:
        queryset = queryset.filter(categories__id__exact=cat_id)
    return queryset
