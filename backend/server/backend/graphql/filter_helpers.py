from typing import List, Mapping, Optional

from django.db.models import QuerySet
from django.contrib.postgres.search import SearchVector
from graphql import GraphQLError

from backend.model.translation_collection import translation_tables, graph_info_translation_tables


def skip_none(func):
    def wrapper(*args, **kwargs):
        if any(value is None for value in kwargs.values()):
            return args[0]
        else:
            return func(*args, **kwargs)

    return wrapper


def get_search_text(filter_content: Mapping) -> Optional[str]:
    search_text: Optional[str] = filter_content.get('search_text', None)
    if search_text is not None and not isinstance(search_text, str):
        raise GraphQLError('The search text must be a string.')
    return search_text


def get_category_ids(filter_content: Mapping) -> Optional[List[str]]:
    category_ids: Optional[str] = filter_content.get('category_ids', None)
    if category_ids is not None and \
            not (isinstance(category_ids, List) and all(isinstance(cat, str) for cat in category_ids)):
        raise GraphQLError('The categories must be a list of strings.')
    return category_ids


tutorial_content_search_vector_parts = ['%s__title', '%s__abstract', '%s__content_md', ]
content_search_vector_attrs = ['url', 'name']


@skip_none
def tutorial_content_search(queryset: QuerySet, search_text: str) -> QuerySet:
    return queryset.annotate(
        search=SearchVector(
            *(part % trans_type
              for trans_type in translation_tables
              for part in tutorial_content_search_vector_parts),
            *content_search_vector_attrs
        )
    ).filter(search=search_text)


@skip_none
def category_id_filter(queryset: QuerySet, category_ids: List[str]) -> QuerySet:
    for cat_id in category_ids:
        queryset = queryset.filter(categories__id__exact=cat_id)
    return queryset


graph_content_search_vector_parts = ['%s__abstract_md', '%s__title']


@skip_none
def graph_content_search(queryset: QuerySet, search_text: str) -> QuerySet:
    return queryset.annotate(
        search=SearchVector(
            *(part % trans_type
              for trans_type in graph_info_translation_tables
              for part in graph_content_search_vector_parts),
            *content_search_vector_attrs
        )
    ).filter(search=search_text)
