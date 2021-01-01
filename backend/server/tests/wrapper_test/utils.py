from backend.intel_wrappers.wrapper_bases import AbstractWrapper
from tests.utils import EmptyValue


def make_new_model_test_helper(wrapper_instance: AbstractWrapper, variables: dict):
    wrapper_instance = wrapper_instance.set_variables(**variables)
    wrapper_instance.make_new_model()

    wrapper_model = wrapper_instance.model

    assert wrapper_model is not None

    for field_name, value in variables.items():
        model_field_value = getattr(wrapper_model, field_name, EmptyValue)
        assert not model_field_value == EmptyValue
