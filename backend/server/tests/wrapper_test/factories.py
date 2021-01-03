import random
from typing import Tuple, Callable, Sequence, Type, TypeVar, Mapping, Optional

from django.db.models import Model

from backend.intel_wrappers.intel_wrapper import CategoryWrapper, TutorialAnchorWrapper, UserWrapper, CodeWrapper, \
    GraphWrapper
from backend.intel_wrappers.wrapper_bases import AbstractWrapper
from backend.model.TutorialRelatedModel import GraphPriority
from backend.model.UserModel import ROLES

_T = TypeVar('_T', bound=AbstractWrapper)
WrappersFactoryType = Tuple[Callable[[], Sequence[_T]], Callable[[], None]]
WrapperFactoryType = Tuple[Callable[[], _T], Callable[[], None]]


def _general_wrappers_factory(wrapper_type: Type[_T], params: Sequence[Mapping]) -> WrappersFactoryType:
    _wrappers: Optional[Sequence] = None

    def _ws_maker() -> Sequence[_T]:
        nonlocal _wrappers
        _wrappers = [
            wrapper_type().load_model(
                wrapper_type.model_class.objects.create(**param)
            ) for param in params
        ]
        return _wrappers

    def _ws_destructor() -> None:
        for wrapper in _wrappers:
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


def tutorial_anchor_wrappers_factory(url_template: str, name_template: str, num: int,
                                     rank_base_num: int = 500) -> WrappersFactoryType:
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


def secondary_model_parser(secondary_models: Mapping[str, Tuple[Type[AbstractWrapper], Mapping]]) -> Mapping:
    if secondary_models is None:
        return {}

    return {
        key: value[0].model_class.objects.create(**value[1])
        for key, value in secondary_models.items()
    }


def collection_model_parser(collection_models: Mapping) -> Mapping:
    if collection_models is None:
        return {}


def _general_wrapper_factory(wrapper_type: Type[_T], params: Mapping,
                             secondary_models_info: Mapping[str, Tuple[Type[AbstractWrapper], Mapping]] = None,
                             collection_models_info: Mapping[str, Tuple] = None) -> WrapperFactoryType:
    _wrapper: Optional[_T] = None
    _secondary_models: Optional[Mapping] = None
    _collection_models: Optional[Mapping] = None

    def _w_maker() -> _T:
        nonlocal _wrapper, _secondary_models, _collection_models
        _secondary_models = secondary_model_parser(secondary_models_info)
        _collection_models = collection_model_parser(collection_models_info)

        model_instance, created = wrapper_type.model_class.objects.get_or_create(
            **params,
            **_secondary_models,
            **_collection_models
        )
        _wrapper = wrapper_type().load_model(
            model_instance
        )

        return _wrapper

    def _w_destructor() -> None:
        if _wrapper is not None:
            _wrapper.delete_model()
        for value in _secondary_models.values():
            value.delete()
        for value in _collection_models.values():
            value.delete()

    return _w_maker, _w_destructor


def tutorial_anchor_wrapper_factory(url_template: str, name_template: str,
                                    rank_base_num: int = 500) -> WrapperFactoryType:
    return _general_wrapper_factory(TutorialAnchorWrapper, {
        'url': url_template,
        'name': name_template,
        'level': rank_base_num,
        'section': random.randint(0, 9)
    })


def code_wrapper_factory(code_content: str,
                         tutorial_url_template: str, tutorial_name_template: str,
                         level: int = 500) -> WrapperFactoryType:
    return _general_wrapper_factory(
        CodeWrapper, {'code': code_content}, secondary_models_info={
            'tutorial': (TutorialAnchorWrapper, {
                'url': tutorial_url_template,
                'name': tutorial_name_template,
                'level': level,
                'section': random.randint(0, 9)
            })
        }
    )


def graph_wrapper_factory(graph_url: str, graph_name: str, graph_json: Mapping,
                          priority: int = GraphPriority.MAIN) -> WrapperFactoryType:
    return _general_wrapper_factory(
        GraphWrapper, {
            'url': graph_url,
            'name': graph_name,
            'cyjs': graph_json,
            'priority': priority,
            'is_published': True
        }
    )


def wrapper_to_model_helper(wrapper: _T) -> Model:
    return wrapper.model
