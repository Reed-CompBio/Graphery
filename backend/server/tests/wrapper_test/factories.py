import random
from typing import Tuple, Callable, Sequence, Type, TypeVar, Mapping

from django.db.models import Model

from backend.intel_wrappers.intel_wrapper import CategoryWrapper, TutorialAnchorWrapper, UserWrapper
from backend.intel_wrappers.wrapper_bases import AbstractWrapper
from backend.model.UserModel import ROLES

_T = TypeVar('_T', bound=AbstractWrapper)
FactoryType = Tuple[Callable[[], Sequence[_T]], Callable[[Sequence[_T]], None]]


def _general_factory(wrapper_type: Type[_T], params: Sequence[Mapping]) -> FactoryType:
    def _maker() -> Sequence[_T]:
        return [
            wrapper_type().load_model(
                wrapper_type.model_class.objects.create(**param)
            ) for param in params
        ]

    def _destructor(wrappers: Sequence[_T]) -> None:
        for wrapper in wrappers:
            wrapper.delete_model()

    return _maker, _destructor


def user_wrapper_factory(username_template: str, email_template: str, num: int) -> FactoryType:
    return _general_factory(
        UserWrapper, [
            {
                'username': username_template.format(i),
                'email': email_template.format(i),
                'password': 'password',
                'role': ROLES.VISITOR
            } for i in range(num)
        ]
    )


def category_wrapper_factory(template: str, num: int) -> FactoryType:
    return _general_factory(CategoryWrapper, [
        {'category': template.format(i)} for i in range(num)
    ])


def tutorial_anchor_wrapper_factory(url_template: str, name_template: str, num: int, rank_base_num: int = 500) -> FactoryType:
    return _general_factory(TutorialAnchorWrapper, [
        {
            'url': url_template.format(i),
            'name': name_template.format(i),
            'level': rank_base_num + i,
            'section': random.randint(0, 9)
        } for i in range(num)
    ])


def wrappers_to_models(wrappers: Sequence[_T]) -> Sequence[Model]:
    return [wrapper.model for wrapper in wrappers]
