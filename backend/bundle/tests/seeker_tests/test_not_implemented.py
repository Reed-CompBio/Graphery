# Copyright 2019 Ram Rachum and collaborators.
# This program is distributed under the MIT license.

import textwrap
import sys

import pytest

from bundle import seeker
from bundle.seeker import pycompat


def test_rejecting_coroutine_functions():
    if sys.version_info[:2] <= (3, 4):
        pytest.skip()

    code = textwrap.dedent('''
    async def foo(x):
        return 'lol'
    ''')
    namespace = {}
    exec(code, namespace)
    foo = namespace['foo']

    assert pycompat.iscoroutinefunction(foo)
    assert not pycompat.isasyncgenfunction(foo)
    with pytest.raises(NotImplementedError):
        seeker.tracer()(foo)


def test_rejecting_async_generator_functions():
    if sys.version_info[:2] <= (3, 6):
        pytest.skip()

    code = textwrap.dedent('''
    async def foo(x):
        yield 'lol'
    ''')
    namespace = {}
    exec(code, namespace)
    foo = namespace['foo']

    assert not pycompat.iscoroutinefunction(foo)
    assert pycompat.isasyncgenfunction(foo)
    with pytest.raises(NotImplementedError):
        seeker.tracer()(foo)


