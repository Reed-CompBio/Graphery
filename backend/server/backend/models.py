from .model.UserModel import \
    UserNameValidator, ROLES, UserManager, User
from .model.TutorialRelatedModel import \
    Category, Tutorial, Graph, Code, ExecResultJson
from .model.TranslationModels import *

import django_filters


class CategoryFilter(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter()

    class Meta:
        model = Tutorial
        fields = ['categories', ]
