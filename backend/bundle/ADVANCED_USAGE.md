# Advanced Usage #

Use `watch_explode` to expand values to see all their attributes or items of lists/dictionaries:

```python
from bundle.seeker import tracer

@tracer(watch_explode=('foo', 'self'))
```

`watch_explode` will automatically guess how to expand the expression passed to it based on its class. You can be more specific by using one of the following classes:

```python

from bundle.seeker import tracer
from bundle.seeker import Attrs, Keys, Indices

@tracer(
    Attrs('x'),    # attributes
    Keys('y'),     # mapping (e.g. dict) items
    Indices('z'),  # sequence (e.g. list/tuple) items
)
```

Exclude specific keys/attributes/indices with the `exclude` parameter, e.g. `Attrs('x', exclude=('_foo', '_bar'))`.

Add a slice after `Indices` to only see the values within that slice, e.g. `Indices('z')[-3:]`.

```console
# This makes PySnooper not do any snooping
# But I am not sure why you wanna do this 
$ export SEEKER_DISABLED=1 
```

This will output lines like:

```
Modified var:.. foo[2] = 'whatever'
New var:....... self.baz = 8
```

On multi-threaded apps identify which thread are snooped in output:

```python
@tracer(thread_info=True)
```

PySnooper supports decorating generators.

If you decorate a class with `tracer`, it'll automatically apply the decorator to all the methods. (Not including properties and other special cases.)

You can also customize the repr of an object:

```python
from bundle.seeker import tracer
import numpy

def large(l):
    return isinstance(l, list) and len(l) > 5

def print_list_size(l):
    return f'list(size={len(l)})'

def print_ndarray(a):
    return f'ndarray(shape={a.shape}, dtype={a.dtype})'

@tracer(custom_repr=((large, print_list_size), (numpy.ndarray, print_ndarray)))
def sum_to_x(x):
    l = list(range(x))
    a = numpy.zeros((10,10))
    return sum(l)

sum_to_x(10000)
```

You will get `l = list(size=10000)` for the list, and `a = ndarray(shape=(10, 10), dtype=float64)` for the ndarray.
The `custom_repr` are matched in order, if one condition matches, no further conditions will be checked.

Variables and exceptions get truncated to 100 characters by default. You
can customize that:

```python
from bundle.seeker import tracer

@tracer(max_variable_length=200)
```

You can also use `max_variable_length=None` to never truncate them.

Use `relative_time=True` to show timestamps relative to start time rather than
wall time.