## User Server API 

### Current API 

```python
{
    'line': line, 
    'variables': {
        'identity': {
            'type': 'some_type',
            'color': 'some_color_hex',
            'repr': 'some_repr'
        }
    }
}
```

The line is the line number of current execution. Say the current line is 17, the variables are showing the list of variable in the environment after the line is executed. 

`identity` is built from `(prefix, variable_name)`. The prefix is the string representation of a class or a function. The variable name is the variable name of the variable. This format is going to create namespace for every variable and avoid errors on frontend parsing. The identity itself is a string. The two components are separated by `#`. 

`type` is an after-thought added at the end of the first development cycle. This was intended to distinguish graph objects from regular objects. 

`color` is the color hex with which the variable is going to be identified on the frontend. 

`repr` is the string representation of the variable, that is, the value of the variable. 

### Proposed API 

```python
[
    {
        'line': line, 
        'variables': {
            'identity': {
                'type': 'some_type',
                'color': 'some_color_hex',
                'repr': 'some_repr'
                'properties': {
                    'property_1': str or number,
                    ...
                }
            }
        }, 
        'accesses': [
            {
                'type': 'some_type',
                'color': 'some_color_hex',
                'repr': 'some_repr',
                'properties': {
                    'property_1': str or number,
                    ...
                }
            },
        ],
        'order': ['identity1', 'identity2', ...]
    },
    ...
]
```

The `identity` should be built from an `Sequence` of strings by following rules.

The `Sequence` mush have a length greater than `2` to avoid name duplication. One with length greater than `2` is also acceptable, as long as the frontend and the backend can communicate. The length is going probably going to get longer to cope with potential name duplication, since adding more string we are creating new namespaces. The last item of the `Sequence` must be the name of the variable. This must be reinforced by both the frontend and the backend. 

When the components in the `Sequence` are connected by a separator, they become the identity. The separator is now proposed to be `u'\u200b@'`, where `u'\u200b'` is an empty char that's almost impossible to appear in the domain of possible components and `u'@'` is to make sure it's human readable during debugging. 

The `identity` should be decoded in the following way. Get the namespaces and the variable name by removing the separator, select useful namespaces, and display the variable with selected ones. 

The `type` should be a enum(mapping) that has the following values. 

```python
{
    Node: 'Node',
    Edge: 'Edge',
    str: 'String',
    List: 'List',
    Tuple: 'Tuple',
    Deque: 'Deque',
    #  Counter: 'Counter',
    tyep(None): 'None',
    Set: 'Set',  # which includes Set, set, KeyView(dict_keys), ItemView(dict_items), frozenset, MutableSet
    Mapping: 'Mapping',  # which includes mappingproxy (not sure what that is), MutableMapping, dict 
    Sequence: 'Sequence',  # which includes tuple, str, range, memoryview, MutableSequence, list, bytearray
    #  ByteString: 'ByteString',  # which is optional in this version 
    object: 'Object'  # any other things
}
```

The type string should follow the naming convention for a class. 

The order in this dictionary matters. Since if a string is matched as a sequence, the frontend is probably going to unfold the elements (in this case the chars). 

The hex color should be chose in a way that's friendly to color blind people. It's not guaranteed that all colors are friendly. The author should try to expand the palette as much as possible. 

`repr` should be a string representation of the value. The `repr` should be formatted according to the `type` field. Then, if the `__repr__` or `__str__` function is overridden in a instance, the program should use those. It should prefer `__repr__` over `__str__`. Otherwise, the ugly default representation should be used. 

The item is `property` which is a graph-element-specific item. That is, only graph elements have this item. The `property` contains the properties that's needed to be displayed on the tooltips in the Cytoscape window. Currently, the value of the `property` mapping should only be a string or a number. 

The `accesses` contains a list of accessed values from some function calls. If a function is marked with a decorator `look_at`, the return value of the function will be recorded. 

The new variable list is going to bring up the changed variables. So `order` is a new field that going to specify the order of the variables on the variable list. Since the dictionary used in the variable list preserves the insertion order, one way to get around `order` field is by deleting the variable and add it back as if it's a new record. 

## Frontend 

The transition of the variable list can be cover by [native `<transition-group>`](https://vuejs.org/v2/guide/transitions.html#List-Transitions) tag. 
