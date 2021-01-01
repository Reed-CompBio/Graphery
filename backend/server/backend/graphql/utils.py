from typing import TypeVar, Type, List, Iterable

from graphql import GraphQLError

from backend.intel_wrappers.wrapper_bases import AbstractWrapper


_T = TypeVar('_T', bound=AbstractWrapper)


def process_model_wrapper(model_wrapper_class: Type[_T], **kwargs) -> _T:
    wrapper_instance = model_wrapper_class().set_variables(**kwargs)
    wrapper_instance.finalize_model()
    if wrapper_instance.model is None:
        raise GraphQLError('Internal Error: Cannot create model at this time.')

    return wrapper_instance


_S = TypeVar('_S', bound=AbstractWrapper)


def get_wrappers_by_ids(model_wrapper_class: Type[_S],
                        model_info: Iterable[str]) -> List[_S]:
    # noinspection PyArgumentList
    wrapper_collection = [get_wrapper_by_id(model_wrapper_class, the_info)
                          for the_info in model_info]
    return wrapper_collection


def get_wrapper_by_id(model_wrapper_class: Type[_S], model_id: str) -> _S:
    return model_wrapper_class().load_model(model_wrapper_class.model_class.objects.get(id=model_id))
