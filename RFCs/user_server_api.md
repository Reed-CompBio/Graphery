# User Server API 

## Current API 

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

## Proposed API 

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

The `identity` should be built from an `Sequence` of strings by following rules.

The `Sequence` mush have a length greater than `2` to avoid name duplication. One with length greater than `2` is also acceptable, as long as the frontend and the backend can communicate. The length is going probably going to get longer to cope with potential name duplication, since adding more string we are creating new namespaces. The last item of the `Sequence` must be the name of the variable. This must be reinforced by both the frontend and the backend. 

When the components in the `Sequence` are connected by a separator, they become the identity. The separator is now proposed to be `u'\u200b_'`, where `u'\u200b'` is an empty char that's almost impossible to appear in the domain of possible components and `'_'` is to make sure it's human readable during debugging. 

The `identity` should be decoded in the following way. Get the namespaces and the variable name by removing the separator, select useful namespaces, and display the variable with selected ones. 

The `type` should be a enum(mapping) that has the following values. 

```python
{
    None: 'None',
    
}
```
