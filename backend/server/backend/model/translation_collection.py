from typing import Optional

from django.db.models import Model

translation_tables = []

translation_types = []

translation_table_mapping = {}


def add_trans_type(cls: type):
    translation_types.append(cls)
    return cls


def add_trans_table(cls: type):
    cls_name: str = cls.__name__.lower()
    translation_tables.append(cls_name)
    translation_table_mapping[cls_name] = cls
    return cls


def process_trans_name(trans_code: str) -> str:
    return trans_code.replace('-', '').replace('_', '').lower()


def process_graph_trans_name(trans_code: str) -> str:
    return f"{process_trans_name(trans_code)}graph"


def has_translation(trans_code: str) -> bool:
    return trans_code in translation_tables


def get_translation_table(table_name: str) -> Optional[Model]:
    table_name = process_trans_name(table_name)
    return translation_table_mapping.get(table_name, None)
