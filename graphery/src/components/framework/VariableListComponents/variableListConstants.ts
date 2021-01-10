import * as constants from 'constants';

export const _EMPTY_VALUE_STRING = '<EMPTY>';
export const _ACCESSED_VARIABLE_OBJ_LABEL = 'Accessed';
export const _EMPTY_TYPE_STRING = 'Empty';

export const _COLOR_HEADER = 'color';
export const _REPR_HEADER = 'repr';
export const _TYPE_HEADER = 'type';

type ArrayOfFixedLength<T extends any, N extends number> = readonly T[] & {
  length: N;
};

export const _SINGULAR_TYPES = ['Number', 'String', 'Node', 'Edge', 'None'];
export const _SINGULAR_TYPE_ICON = ['', '', '', '', ''];

export const _LINEAR_CONTAINER_TYPES = [
  'List',
  'Tuple',
  'Deque',
  'Set',
  'Sequence',
];
export const _LINEAR_CONTAINER_TYPE_ICON = ['', '', '', '', ''];

export const _PAIR_CONTAINER_TYPES = ['Counter', 'Mapping'];
export const _PAIR_CONTAINER_TYPE_ICON = ['', ''];

export const _GRAPH_OBJECT_TYPES = ['Node', 'Edge'];

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
    zipArraysToObject<5>(
      _SINGULAR_TYPES as ArrayOfFixedLength<string, 5>,
      _SINGULAR_TYPE_ICON as ArrayOfFixedLength<string, 5>,
      5
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
