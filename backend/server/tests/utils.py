import re


def camel_to_snake(var_name: str) -> str:
    var_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', var_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', var_name).lower()


class EmptyValue:
    pass


class AnyValue:
    def __eq__(self, other):
        return True


AnyValue = AnyValue()


class AnyNoneEmptyValue:
    def __eq__(self, other):
        return bool(other)


AnyNoneEmptyValue = AnyNoneEmptyValue()
