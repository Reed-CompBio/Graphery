# Result JSON API

## API versions

*   <a href="#3-0">3.0</a>
*   <a href="#2.0">2.0</a>
*   <a href="#1-0">1.0 (Depricated)</a>

## 3.0 API {#3-0}

Credit: a lot of internal changes were inspired by [PyTutor](https://github.com/okpy/pytutor/). 

```typescript
type python_graph_object_type = "Node" | "Edge";

type python_object_type =
  | "Number"
  | "String"
  | "List"
  | "Tuple"
  | "Deque"
  | "None"
  | "Set"
  | "Mapping"
  | "Sequence"
  | "Object";

type special_object_type = "Init" | "Ref";

type object_type =
  | python_graph_object_type
  | python_object_type
  | special_object_type;

type object_identity_seperator = "\u200b@";

type object_identity_type = `${string}${object_identity_seperator}${string}`;

interface compositional_object_identity_type {
  type: object_type;
  color: string;
  repr: string;
  properties?: {
    graph_id: string;
    [key: string]: string | number;
  };
  python_id: number;
}

interface record_type {
  line: number;
  variables: {
    [key: string]: compositional_object_identity_type;
  };
  accesses?: compositional_object_identity_type[];
  variable_orders?: string[];
  stdout?: string;
}

type record_array_type = record_type[];
```

Examples:

```typescript

let an_example: compositional_object_identity_type = {
  type: "Node",
  color: "#3A5F99",
  repr: "animal node",
  properties: {
    graph_id: "#19",
    degree: 19,
  },
  python_id: 4411533616,
};

let two_example: compositional_object_identity_type = {
  type: "Number",
  color: "#334766",
  repr: "20",
  python_id: 4411533616,
};

let one_more_example: record_type = {
  line: 18,
  variables: {
    "main\u200b@test_var": an_example,
  },
  accesses: [two_example],
  stdout: "hello world! \n",
};
```

## 2.0 API {#2-0}

A _record array_ looks like this. Each element in the record array is called _record object_ or simply _record_. 

```python
record_array = [
    {
        'line': 18, 
        'variables': {
            '<identity>': {
                'type': 'some_type',
                'color': 'some_color_hex',
                'repr': 'some_repr',
                'id': 'graph_element_id',
                'properties': {
                    'property_1': str or number,
                    ...
                },
                "python_id": 123456789
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
                },
                "python_id": 123456789
            },
        ],
        'order': ['identity1', 'identity2', ...]
    },
    ...
]
```

### `line`

The `line` field indicates which line this object is referencing. The type is `int`. 

### `variables`

The `variables` field indicates which variables are accessed in this line. It's a `dict` type, or `object` in JS. The members are detailed below. 

#### `<identity>`

The `<identity>` is going to be replaced by a string built from an `Sequence` of strings by the following rules.

First, we need a  `ideantity` `Sequence`, which has a length greater than `2` to avoid namespace collision. For example, a tuple `('test_function', 'test_var')`. One with length greater than `2` is also acceptable, as long as the frontend and the backend agree. The length is probably going to get longer to cope with potential name duplication, since by adding more string we are creating new namespaces. The last item of the `Sequence` must be the name of the variable, which is to be displayed on the screen. This must be reinforced by both the frontend and the backend. 

When the elements in the `Sequence` are connected by a separator, they become a _textual variable identity_, which is going to replace the `<identity>`'s place. The separator is now proposed to be `u'\u200b@'`, where `u'\u200b'` is an [empty char](https://unicode-table.com/en/200B/) that's almost impossible to appear in the domain of possible components and `u'@'` is to make sure it's human readable during debugging. 

The `<identity>` should be decoded in the following way by removing the separator in a textual variable identity. Two `<identity>`s are considered as the same when they have the same namespaces __and__ the same name For future discussions, the content in a `<identity>` field, ie. the object of `<identity>`, is called _compositional variable identity_. 

##### `type`

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
    type(None): 'None',
    Set: 'Set',  # which includes Set, set, KeyView(dict_keys), ItemView(dict_items), frozenset, MutableSet
    Mapping: 'Mapping',  # which includes mappingproxy (not sure what that is), MutableMapping, dict 
    Sequence: 'Sequence',  # which includes tuple, str, range, memoryview, MutableSequence, list, bytearray
    #  ByteString: 'ByteString',  # which is optional in this version 
    object: 'Object'  # the wildcard that matches everything else 
}
```

Some additional types are added to provide more information: 

```python
[
    'init',
    'reference',
]
```

`init` type indicates the element has not been initialized yet, which should only be used on the variables in the first record. 

`reference` type indicates the current object is a reference, and guarantees that the object appears in the previous stack trace. To obtain the detail of the object, the program should look backward.  (we will talk about this later)

The `type` string should follow the naming convention of a Python class. 

The order in this dictionary matters. Since if a string (`str` type) is matched as a sequence (`Sequence` type), the frontend is probably going to unfold the elements (in this case the chars, so a literal `hello` will be displayed as `[H, E, L, L, O]`). 

The types can be further divided into subcategories: 
```python
_SINGULAR_MAPPING = {
    Number: 'Number',
    str: 'String',
    Node: 'Node',
    Edge: 'Edge',
    type(None): 'None',
}
# and 
_LINEAR_CONTAINER_MAPPING = {
    List: 'List',
    Tuple: 'Tuple',
    Deque: 'Deque',
    Set: 'Set',  # which includes Set, set, KeyView(dict_keys), ValueView(dict_values), ItemView(dict_items),
    # frozenset, MutableSet
    Sequence: 'Sequence',  # which includes tuple, str, range, memoryview, MutableSequence, list, bytearray
}
# and 
_PAIR_CONTAINER_MAPPING = {
    Counter: 'Counter',
    Mapping: 'Mapping',  # which includes mappingproxy (not sure what that is), MutableMapping, dict
}
# and 
_WILDCARD_MAPPING = {
  object: 'Object'
}
# so 
_TYPE_MAPPING = {
        # simple individuals
        **_SINGULAR_MAPPING,
        # simple linear containers
        **_LINEAR_CONTAINER_MAPPING,
        # simple pair containers
        **_PAIR_CONTAINER_MAPPING,
        # wildcard
       	** _WILDCARD_MAPPING
    }
```
##### `repr`

Types in the singular mapping should be checked first. And they will be converted into strings when being as the value of `repr` field. 

For types in the linear container mapping, we are using recursive resolution method for the elements in the object, meaning the every memeber in a linear container will go through the resolution function again. The `repr` field of the objects of these types will be a array of compositional variable identities. 

Since JSON doesn't support keys being objects, objects in the pair container cannot be represented in key-value pair as they do in the python. So the elements, contents of both key and value in the key-value pair, in objects of these types will also go through recursive resolution. As a result, we are using an array to represent the key-value pairs in each pair container. The `repr` field will be a array of objects with object having only two key-value pairs, whose keys are `key` and `value` respectively, and values are compositional variable identities. 

Here is an example: 

```python
# for linear containers 
[
  	{
        "type": "some_type",
        "color": "some_color_hex",
        "repr": "some_repr",
        "id": "graph_element_id",
        "properties": {
            "property_1": "str or number"
            ...
        },  # (required only by graph objects like nodes and edges)
        "python_id": 123456789
    }, 
    {
        "type": "some_type",
        "color": "some_color_hex",
        "repr": "some_repr",
        "id": "graph_element_id",
        "properties": {
            "property_1": "str or number"
            ...
        },
        "python_id": 123456789
    }
]

# for pair containers 
[
    {
        "key": {
            "type": "some_type",
            "color": "some_color_hex",
            "repr": "some_repr",
            "id": "graph_element_id",
            "properties": {
                "property_1": "str or number"
                ...
            },
            "python_id": 123456789
        }, 
        "value": {
            "type": "some_type",
            "color": "some_color_hex",
            "repr": "some_repr",
            "id": "graph_element_id",
            "properties": {
                "property_1": "str or number"
                ...
            },
            "python_id": 123456789
        }
    },
    ...
]
```

Hence, we can preserve the key-value pairs and use recursion to generate general object representations. 

`repr` should be a string representation of the value. The `repr` should be formatted according to the `type` field. Then, if the `__repr__` or `__str__` function is overridden in a instance, the program should use those. It should prefer `__repr__` over `__str__`. Otherwise, the ugly default representation should be used. 

##### `color`

The `color` is used to in the visualization. The value of `color` must be a string of hex color. The hex color should be chose in a way that's friendly to color blind people. It's not guaranteed that all colors are friendly. The author should try to expand the palette as much as possible. 

##### `id`

The field `id` is the id of the graph element. The field facilitates the interaction with and is required by the Cytoscape module. 

##### `property` (only bounded to graph objects like nodes and edges)

The item is `property` which is a graph-element-specific item. That is, only graph elements have this item. The `property` contains the properties that's needed to be displayed on the tooltips in the Cytoscape window. Currently, the value of the `property` mapping should only be a string or a number. 

##### `python_id`

The `python_id` field is to collect the result of `id()` of the object. When there is a recursive structure, the repeated objects can refer to the previous object. 

##### `accesses`

The `accesses` contains a list of accessed values from some function calls. If a function is marked with a decorator `look_at`, the return value of the function will be recorded. 

The new variable list is going to bring up the changed variables. So `order` is a new field that going to specify the order of the variables on the variable list. Since the dictionary used in the variable list preserves the insertion order, one way to get around `order` field is by deleting the variable and add it back as if it's a new record. 

## 1.0 API (Depricated) {#1-0}

```python
record_array = [
  {
      'line': 17, 
      'variables': {
          'identity': {
              'type': 'some_type',
              'color': 'some_color_hex',
              'repr': 'some_repr'
          }
      }
  }, 
  ...
]
```

The `line` variable is the line number of current execution. Say the current line is 17, the variables are showing the list of variable in the environment after the line is executed. 

`identity` is built from `(prefix, variable_name)`. The prefix is the string representation of a class or a function. The variable name is the variable name of the variable. This format is going to create namespace for every variable and avoid errors on frontend parsing. The identity itself is a string. The two components are separated by `#`. 

`type` is an after-thought added at the end of the first development cycle. This was intended to distinguish graph objects from regular objects. 

`color` is the color hex with which the variable is going to be identified on the frontend. 

`repr` is the string representation of the variable, that is, the value of the variable. 

## 