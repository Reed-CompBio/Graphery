from typing import Optional

translation_tables = []

translation_table_mapping = {}


def add_trans_table(cls: type):
    cls_name: str = cls.__name__.lower()
    translation_tables.append(cls_name)
    translation_table_mapping[cls_name] = cls
    return cls


def get_translation_table(table_name: str) -> Optional['TranslationBase']:
    table_name = table_name.replace('-', '').replace('_', '').lower()
    return translation_table_mapping.get(table_name, None)
