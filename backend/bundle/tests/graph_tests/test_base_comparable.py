from typing import Callable

import pytest
from operator import eq, gt, ge, lt, le, ne

from bundle.GraphObjects.Base import Comparable


class DefaultTestComparable(Comparable):
    def __init__(self, identity: str):
        super(DefaultTestComparable, self).__init__(identity)


def test_hash():
    instance = DefaultTestComparable('a')
    assert instance.hash_cache is None
    hash_value = hash(instance)
    assert hash_value == instance.hash_cache


@pytest.mark.parametrize('left, right, operator, result', [
    pytest.param(
        0, 1, eq, False
    ),
    pytest.param(
        1, 1, eq, True
    ),
    pytest.param(
        0, 1, lt, True
    ),
    pytest.param(
        0, 1, le, True
    ),
    pytest.param(
        1, 1, le, True
    ),
    pytest.param(
        2, 1, gt, True
    ),
    pytest.param(
        2, 1, ge, True
    ),
    pytest.param(
        2, 2, ge, True
    ),
    pytest.param(
        2, 1, ne, True
    ),
    pytest.param(
        2, 2, ne, False
    )
])
def test_comparable_comparison(left, right, operator: Callable, result: bool):
    assert operator(DefaultTestComparable(left), DefaultTestComparable(right)) == result
