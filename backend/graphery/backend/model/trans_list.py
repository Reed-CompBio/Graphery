from typing import Optional

translation_tables = ('zhcn', )

translation_table_mapping = {}


def add_trans_table(cls):
    translation_table_mapping[cls.__name__] = cls
    return cls


def get_translation_table(table_name: str) -> Optional['TranslationBase']:
    table_name = table_name.replace('-', '').replace('_', '').lower()
    return translation_table_mapping.get(table_name, None)
