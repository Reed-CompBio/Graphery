# Copyright 2019 Ram Rachum and collaborators.
# This program is distributed under the MIT license.

from bundle import seeker

from .bar import bar_function


@seeker.tracer(depth=2, only_watch=False)
def foo_function():
    z = bar_function(3)
    return z