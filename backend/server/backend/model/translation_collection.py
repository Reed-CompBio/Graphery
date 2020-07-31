from typing import Optional, Type, List, MutableMapping

from django.db.models import Model
from graphene import ObjectType

translation_tables: List[str] = []

translation_types: List[Type[ObjectType]] = []

# noinspection PyUnresolvedReferences
translation_table_mapping: MutableMapping[str, Type['TranslationBase']] = {}

graph_info_translation_tables: List[str] = []

# noinspection PyUnresolvedReferences
graph_info_translation_table_mapping: MutableMapping[str, Type['GraphTranslationBase']] = {}


def add_trans_type(cls: Type[ObjectType]):
    translation_types.append(cls)
    return cls


def add_trans_table(cls: Type):
    cls_name: str = cls.__name__.lower()
    translation_tables.append(cls_name)
    translation_table_mapping[cls_name] = cls
    return cls


def add_graph_info_trans_table(cls: Type):
    cls_name: str = cls.__name__.lower()
    graph_info_translation_tables.append(cls_name)
    graph_info_translation_table_mapping[cls_name] = cls
    return cls


def process_trans_name(trans_code: str) -> str:
    return trans_code.replace('-', '').replace('_', '').lower()


def process_graph_info_trans_name(trans_code: str) -> str:
    return f"{process_trans_name(trans_code)}GraphContent".lower()


def has_translation(trans_code: str) -> bool:
    """
    check whether the translation represented by the trans_code
    is created. This does not mean a particular translation
    exists in the translation table.
    :param trans_code:
    :return:
    """
    return process_trans_name(trans_code) in translation_tables


def has_graph_info_translation(trans_code: str) -> bool:
    return process_graph_info_trans_name(trans_code) in translation_tables


def get_translation_table(trans_code: str) -> Optional[Type[Model]]:
    table_name = process_trans_name(trans_code)
    return translation_table_mapping.get(table_name, None)


def get_graph_info_trans_table(trans_code: str) -> Optional[Type[Model]]:
    table_name = process_graph_info_trans_name(trans_code)
    return graph_info_translation_table_mapping.get(table_name, None)
