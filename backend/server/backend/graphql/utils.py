from typing import TypeVar, Type, List, Iterable

from graphql import GraphQLError

from backend.intel_wrappers.intel_wrapper import finalize_prerequisite_wrapper

T = TypeVar('T')


def process_model_wrapper(model_wrapper_class: Type[T], **kwargs) -> T:
    # noinspection PyArgumentList
    wrapper_instance = model_wrapper_class().set_variables(**kwargs)
    finalize_prerequisite_wrapper(wrapper_instance, overwrite=True)
    if wrapper_instance.model is None:
        raise GraphQLError('Internal Error: Cannot create model at this time.')

    return wrapper_instance


S = TypeVar('S')


def get_wrappers_by_ids(model_wrapper_class: Type[S],
                        model_info: Iterable[str]) -> List[S]:

    # noinspection PyArgumentList
    wrapper_collection = [model_wrapper_class().load_model(model_wrapper_class.model_class.objects.get(id=the_info))
                          for the_info in model_info]
    return wrapper_collection
