import random
from typing import Tuple, Callable, Sequence, Type, TypeVar, Mapping

from django.db.models import Model

from backend.intel_wrappers.intel_wrapper import CategoryWrapper, TutorialAnchorWrapper, UserWrapper
from backend.intel_wrappers.wrapper_bases import AbstractWrapper
from backend.model.UserModel import ROLES

_T = TypeVar('_T', bound=AbstractWrapper)
WrappersFactoryType = Tuple[Callable[[], Sequence[_T]], Callable[[Sequence[_T]], None]]
WrapperFactoryType = Tuple[Callable[[], _T], Callable[[_T], None]]


def _general_wrappers_factory(wrapper_type: Type[_T], params: Sequence[Mapping]) -> WrappersFactoryType:
    def _ws_maker() -> Sequence[_T]:
        return [
            wrapper_type().load_model(
                wrapper_type.model_class.objects.create(**param)
            ) for param in params
        ]

    def _ws_destructor(wrappers: Sequence[_T]) -> None:
        for wrapper in wrappers:
            wrapper.delete_model()

    return _ws_maker, _ws_destructor


def user_wrappers_factory(username_template: str, email_template: str, num: int) -> WrappersFactoryType:
    return _general_wrappers_factory(
        UserWrapper, [
            {
                'username': username_template.format(i),
                'email': email_template.format(i),
                'password': 'password',
                'role': ROLES.VISITOR
            } for i in range(num)
        ]
    )


def category_wrappers_factory(template: str, num: int) -> WrappersFactoryType:
    return _general_wrappers_factory(CategoryWrapper, [
        {'category': template.format(i)} for i in range(num)
    ])


def tutorial_anchor_wrappers_factory(url_template: str, name_template: str, num: int, rank_base_num: int = 500) -> WrappersFactoryType:
    return _general_wrappers_factory(TutorialAnchorWrapper, [
        {
            'url': url_template.format(i),
            'name': name_template.format(i),
            'level': rank_base_num + i,
            'section': random.randint(0, 9)
        } for i in range(num)
    ])


def wrappers_to_models_helper(wrappers: Sequence[_T]) -> Sequence[Model]:
    return [wrapper.model for wrapper in wrappers]


def _general_wrapper_factory(wrapper_type: Type[_T], params: Mapping) -> WrapperFactoryType:
    def _w_maker() -> _T:
        return wrapper_type().load_model(
                wrapper_type.model_class.objects.create(**params)
            )

    def _w_destructor(wrapper: _T) -> None:
        wrapper.delete_model()

    return _w_maker, _w_destructor


def tutorial_anchor_wrapper_factory(url_template: str, name_template: str, rank_base_num: int = 500) -> WrapperFactoryType:
    return _general_wrapper_factory(TutorialAnchorWrapper, {
            'url': url_template,
            'name': name_template,
            'level': rank_base_num,
            'section': random.randint(0, 9)
        })


def wrapper_to_model_helper(wrapper: _T) -> Model:
    return wrapper.model
