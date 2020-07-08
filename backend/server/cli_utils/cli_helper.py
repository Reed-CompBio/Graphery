from django.core import management
from django.core.management.commands import loaddata
from django import setup as django_setup

import pathlib
import sys
import os

from prompt_toolkit import print_formatted_text
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

import bundle


def init():
    django_root = pathlib.Path('./')
    if django_root.exists():
        print_formatted_text('found Django server path!')
    else:
        raise AssertionError('Cannot find the Django server module!')
    sys.path.append(str(django_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphery.settings.test")
    django_setup()


if __name__ == '__main__':
    init()
    print_formatted_text('this is the start of input')

    from prompt_toolkit.shortcuts import input_dialog

    prompt('input the path', completer=PathCompleter())

    text = input_dialog(
        title='Input dialog example',
        text='Please type your name:',
        completer=PathCompleter()).run()

    from prompt_toolkit.shortcuts import checkboxlist_dialog
    from django.apps import apps

    Category = apps.get_model('backend', 'Category')
    print(Category)
    values = [(ele, ele.category) for ele in Category.objects.all()]

    results_array = checkboxlist_dialog(
        title="CheckboxList dialog",
        text="What would you like in your breakfast ?",
        values=values
    ).run()
    print(results_array)
