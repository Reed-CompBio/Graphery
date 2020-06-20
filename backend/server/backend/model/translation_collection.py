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


def get_translation_table(table_name: str) -> Optional[Model]:
    table_name = table_name.replace('-', '').replace('_', '').lower()
    return translation_table_mapping.get(table_name, None)
