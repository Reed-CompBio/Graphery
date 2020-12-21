# Sight - see everything (not really) #

**Sight** derives from **PySnooper** but it is not a debugger.

# Example #

We're writing a function that converts a number to binary, by returning a list of bits. Let's snoop on it by adding the `@tracer()` decorator (do ***not*** omit the parenthesis at the end of the `tracer`):

```python
from bundle.seeker import tracer

@tracer(only_watch=False)
def number_to_bits(number):
    if number:
        bits = []
        while number:
            number, remainder = divmod(number, 2)
            bits.insert(0, remainder)
        return bits
    else:
        return [0]

number_to_bits(6)
```
The output to stderr is:

```
Source path:... <input>
Starting var:.. number = 6
                call         3 '''
                line         5 from _pydev_comm.pydev_rpc import make_rpc_client, start_rpc_server, start_rpc_server_and_make_client
                line         6 from _pydev_imps._pydev_saved_modules import thread
New var:....... bits = []
                line         7 
                line         8 start_new_thread = thread.start_new_thread
Modified var:.. number = 3
New var:....... remainder = 0
                line         9 
Modified var:.. bits = [0]
                line         7 
                line         8 start_new_thread = thread.start_new_thread
Modified var:.. number = 1
Modified var:.. remainder = 1
                line         9 
Modified var:.. bits = [1, 0]
                line         7 
                line         8 start_new_thread = thread.start_new_thread
Modified var:.. number = 0
                line         9 
Modified var:.. bits = [1, 1, 0]
                line         7 
                line        10 try:
                return      10 try:
Return value:.. [1, 1, 0]
Elapsed time: 00:00:00.000748
```

Or if you don't want to trace an entire function, you can wrap the relevant part in a `with` block:

<!-- TODO use file to run the snippets instead of iPython -->
```python
from bundle.seeker import tracer
import random

def foo():
    lst = []
    for i in range(10):
        lst.append(random.randrange(1, 1000))

    with tracer(only_watch=False):
        lower = min(lst)
        upper = max(lst)
        mid = (lower + upper) / 2
        print(lower, mid, upper)

foo()
```

which outputs something like:

<!-- TODO use file to run the snippets instead of iPython -->
```
Source path:... <input>
New var:....... lst = [779, 652, 993, 452, 256, 461, 926, 491, 684, 881]
New var:....... i = 9
                line        10 try:
New var:....... lower = 256
                line        11     from code import InteractiveConsole
New var:....... upper = 993
                line        12 except ImportError:
New var:....... mid = 624.5
                line        13     from _pydevd_bundle.pydevconsole_code_for_ironpython import InteractiveConsole
Elapsed time: 00:00:00.000315
```

`tracer` does more than showing you what's changed, it also records the changes. You can get the records by using 

```python
tracer.get_recorder().get_change_list()  # type: List[MutableMapping]
```

For the first code in this doc, the output is 

```
[{'line': 3, 'variables': {('number_to_bits', 'number'): 6}, 'accesses': None}, {'line': 5, 'variables': None, 'accesses': None}, {'line': 6, 'variables': {('number_to_bits', 'bits'): []}, 'accesses': None}, {'line': 7, 'variables': None, 'accesses': None}, {'line': 8, 'variables': {('number_to_bits', 'number'): 3, ('number_to_bits', 'remainder'): 0}, 'accesses': None}, {'line': 9, 'variables': {('number_to_bits', 'bits'): [0]}, 'accesses': None}, {'line': 7, 'variables': None, 'accesses': None}, {'line': 8, 'variables': {('number_to_bits', 'number'): 1, ('number_to_bits', 'remainder'): 1}, 'accesses': None}, {'line': 9, 'variables': {('number_to_bits', 'bits'): [1, 0]}, 'accesses': None}, {'line': 7, 'variables': None, 'accesses': None}, {'line': 8, 'variables': {('number_to_bits', 'number'): 0}, 'accesses': None}, {'line': 9, 'variables': {('number_to_bits', 'bits'): [1, 1, 0]}, 'accesses': None}, {'line': 7, 'variables': None, 'accesses': None}, {'line': 10, 'variables': None, 'accesses': None}]
```

For the second snippet:

```
[{'line': 10, 'variables': {('', 'lst'): [420, 388, 791, 341, 704, 597, 662, 572, 838, 339], ('', 'i'): 9, ('', 'lower'): 339}, 'accesses': None}, {'line': 11, 'variables': {('', 'upper'): 838}, 'accesses': None}, {'line': 12, 'variables': {('', 'mid'): 588.5}, 'accesses': None}, {'line': 13, 'variables': None, 'accesses': None}]
```

# Features #

If stderr is not easily accessible for you, you can redirect the output to a file:

```python
from bundle.seeker import tracer

@tracer(output='/my/log/file.log')
```

You can also pass a stream or a callable instead, and they'll be used.

Tracer will only look for the variables you provided in the watch list, 
ike the following decorators do

```python
from bundle.seeker import tracer

@tracer('foo.bar', 'self.x["whatever"]')
# Or 
@tracer(watch=('foo.bar', 'self.x["whatever"]'))
```

However, if you want to trace all variables in the scope and closure, 
you can use flag `only_watch=False`:

```python
from bundle.seeker import tracer

@tracer(only_watch=False)
``` 

Show snoop lines for functions that your function calls:

```python
from bundle.seeker import tracer

@tracer(depth=2)
```

**See _Advanced Usage_ for more options.** <=


# License #

Copyright (c) 2019 Larry Zeng and collaborators, released under the MIT license.

Credit: Seeker is modified from [PySnooper](https://github.com/cool-RR/PySnooper/).
Copyright (c) 2019 Ram Rachum and collaborators, released under the MIT license.
