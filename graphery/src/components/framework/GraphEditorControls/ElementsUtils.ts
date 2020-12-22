export interface TypedVariableObject {
  type: string;
}

const _GRAPH_TYPE_STRINGS = ['Node', 'Edge'];

export function isGraphElement(value: TypedVariableObject | null) {
  return (
    value &&
    _GRAPH_TYPE_STRINGS.filter(function(item) {
      return item === value.type;
    }).length > 0
  );
}

const _CONTAINER_TYPE_STRINGS = [
  'List',
  'Deque',
  'Tuple',
  'Counter',
  'Set',
  'Mapping',
  'Sequence',
];

export function isContainerElement(value: TypedVariableObject | null) {
  return (
    value &&
    _CONTAINER_TYPE_STRINGS.filter(function(item) {
      return item === value.type;
    }).length > 0
  );
}

const _SINGULAR_TYPE_STRINGS = [
  'Number',
  'String',
  'Node',
  'Edge',
  'None',
  'Object',
];

export function isSingularElement(value: TypedVariableObject | null) {
  return (
    value &&
    _SINGULAR_TYPE_STRINGS.filter(function(item) {
      return item === value.type;
    }).length > 0
  );
}

const _INIT_TYPE_STRING = 'init';

export function isInitElement(value: TypedVariableObject | null) {
  return value && value.type === _INIT_TYPE_STRING;
}

const _IDENTITY_STRING_SEPARATOR = '\u200b@';

export function revertNameCombo(nameCombo: string) {
  const components = nameCombo.split(_IDENTITY_STRING_SEPARATOR);
  return components[components.length - 1];
}
