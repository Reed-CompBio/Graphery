# Copyright 2019 Ram Rachum and collaborators.
# This program is distributed under the MIT license.

from bundle import seeker
from bundle.seeker.utils import ensure_tuple


def test_ensure_tuple():
    x1 = ('foo', ('foo',), ['foo'], {'foo'})
    assert set(map(ensure_tuple, x1)) == {('foo',)}

    x2 = (seeker.Keys('foo'), (seeker.Keys('foo'),),
          [seeker.Keys('foo')], {seeker.Keys('foo')})

    assert set(map(ensure_tuple, x2)) == {(seeker.Keys('foo'),)}





