export const _EMPTY_VALUE_STRING = '<EMPTY>';
export const _ACCESSED_VARIABLE_OBJ_LABEL = 'Accessed';
export const _EMPTY_TYPE_STRING = 'Empty';

export const _LABEL_HEADER = 'label';
export const _COLOR_HEADER = 'color';
export const _REPR_HEADER = 'repr';
export const _TYPE_HEADER = 'type';
export const _PYTHON_ID_HEADER = 'python_id';

export const _PAIR_KEY_HEADER = 'key';
export const _PAIR_VALUE_HEADER = 'value';

export const _GRAPH_ELEMENT_SEPARATOR = ', ';

type ArrayOfFixedLength<T extends any, N extends number> = readonly T[] & {
  length: N;
};

export const _INIT_TYPE_STRING = 'init';
export const _INIT_ICON = 'mdi-help-circle-outline';
export const _REFERENCE_TYPE_STRING = 'reference';

export const _SINGULAR_TYPES = [
  'Number',
  'String',
  'Node',
  'Edge',
  'None',
  'Object',
];
export const _SINGULAR_TYPE_ICON = [
  'mdi-numeric',
  'mdi-alphabetical',
  'mdi-ray-vertex',
  'mdi-ray-start-end',
  'mdi-selection-ellipse',
  'mdi-iframe-variable-outline',
];

export const _LINEAR_CONTAINER_TYPES = [
  'List',
  'Tuple',
  'Deque',
  'Set',
  'Sequence',
];
export const _LINEAR_CONTAINER_TYPE_ICON = [
  'mdi-code-brackets',
  'mdi-code-parentheses',
  'mdi-arrow-collapse-vertical',
  'mdi-set-center',
  'mdi-playlist-minus',
];

export const _PAIR_CONTAINER_TYPES = ['Counter', 'Mapping'];
export const _PAIR_CONTAINER_TYPE_ICON = ['mdi-counter', 'mdi-code-braces'];

export const _GRAPH_NODE_TYPE = 'Node';
export const _GRAPH_EDGE_TYPE = 'Edge';
export const _GRAPH_OBJECT_TYPES = [_GRAPH_NODE_TYPE, _GRAPH_EDGE_TYPE];

function zipArraysToObject<N extends number>(
  keyMap: ArrayOfFixedLength<string, N>,
  valueMap: ArrayOfFixedLength<string, N>,
  length: N,
  out: { [key: string]: string } = {}
) {
  for (let i = 0; i < length; i++) {
    out[keyMap[i]] = valueMap[i];
  }
  return out;
}

export const _TYPE_ICON_ENUM = Object.freeze({
  ...Object.assign(
    zipArraysToObject<6>(
      _SINGULAR_TYPES as ArrayOfFixedLength<string, 6>,
      _SINGULAR_TYPE_ICON as ArrayOfFixedLength<string, 6>,
      6
    )
  ),
  ...Object.assign(
    zipArraysToObject<5>(
      _LINEAR_CONTAINER_TYPES as ArrayOfFixedLength<string, 5>,
      _LINEAR_CONTAINER_TYPE_ICON as ArrayOfFixedLength<string, 5>,
      5
    )
  ),
  ...Object.assign(
    zipArraysToObject<2>(
      _PAIR_CONTAINER_TYPES as ArrayOfFixedLength<string, 2>,
      _PAIR_CONTAINER_TYPE_ICON as ArrayOfFixedLength<string, 2>,
      2
    )
  ),
});
