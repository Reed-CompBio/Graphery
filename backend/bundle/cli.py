from django.core import management
from django.core.management.commands import loaddata
from django.conf import settings
from graphery.graphery.settings import test
from django import setup as django_setup

import pathlib
import sys
import os


def load_data_test():
    django_root = pathlib.Path('../graphery/')
    print(django_root.exists())
    sys.path.append(str(django_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.test")
    # settings.configure(default_settings=test)
    django_setup()
    # management.call_command(loaddata.Command(), 'test',
    #                         app_label='backend')


if __name__ == '__main__':
    load_data_test()
