# PySnooper - Never use print for debugging again #

TODO change introductions 

**PySnooper** is a poor man's debugger.

You're trying to figure out why your Python code isn't doing what you think it should be doing. You'd love to use a full-fledged debugger with breakpoints and watches, but you can't be bothered to set one up right now.

You want to know which lines are running and which aren't, and what the values of the local variables are.

Most people would use `print` lines, in strategic locations, some of them showing the values of variables.

**PySnooper** lets you do the same, except instead of carefully crafting the right `print` lines, you just add one decorator line to the function you're interested in. You'll get a play-by-play log of your function, including which lines ran and   when, and exactly when local variables were changed.

What makes **PySnooper** stand out from all other code intelligence tools? You can use it in your shitty, sprawling enterprise codebase without having to do any setup. Just slap the decorator on, as shown below, and redirect the output to a dedicated log file by specifying its path as the first argument.

# Example #

We're writing a function that converts a number to binary, by returning a list of bits. Let's snoop on it by adding the `@pysnooper.snoop()` decorator:

```python

from bundle import seeker

@seeker.snoop()
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
# TODO add an example 
```

Or if you don't want to trace an entire function, you can wrap the relevant part in a `with` block:

```python

from bundle import seeker
import random

def foo():
    lst = []
    for i in range(10):
        lst.append(random.randrange(1, 1000))

    with seeker.tracer():
        lower = min(lst)
        upper = max(lst)
        mid = (lower + upper) / 2
        print(lower, mid, upper)

foo()
```

which outputs something like:

```
# TODO give an example 
```

# Features #

If stderr is not easily accessible for you, you can redirect the output to a file:

```python
@seeker.tracer(outpuyt='/my/log/file.log')
```

You can also pass a stream or a callable instead, and they'll be used.

Seeker will only look for the variables you provided in the watch list, 
ike the following decorators do

```python
@seeker.tracer('foo.bar', 'self.x["whatever"]')
# Or 
@seeker.tracer(watch=('foo.bar', 'self.x["whatever"]'))
```

However, if you want to trace all variables in the scope and closure, 
you can use flag `only_watch=False`:

```python
@seeker.tracer(only_watch=False)
``` 

Show snoop lines for functions that your function calls:

```python
@seeker.tracer(depth=2)
```

**See _Advanced Usage_ for more options.** <=


# License #

Copyright (c) 2019 Larry Zeng and collaborators, released under the MIT license.

Credit: Seeker is modified from [PySnooper](https://github.com/cool-RR/PySnooper/).
Copyright (c) 2019 Ram Rachum and collaborators, released under the MIT license.
