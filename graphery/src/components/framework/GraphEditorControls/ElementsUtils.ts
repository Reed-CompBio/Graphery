import {
  _GRAPH_OBJECT_TYPES,
  _INIT_TYPE_STRING,
  _LINEAR_CONTAINER_TYPES,
  _PAIR_CONTAINER_TYPES,
  _REFERENCE_TYPE_STRING,
  _SINGULAR_TYPES,
  _TYPE_HEADER,
} from '@/components/framework/VariableListComponents/variableListConstants';

export interface GraphElementType {
  id: string;
  type: string;
}

export function makeIdFromObject(element: GraphElementType) {
  return `#${element['id']}`;
}

export function isGraphElement(element: GraphElementType) {
  return _GRAPH_OBJECT_TYPES.includes(element[_TYPE_HEADER]);
}
export function isSingularElement(element: GraphElementType) {
  return _SINGULAR_TYPES.includes(element[_TYPE_HEADER]);
}
export function isLinearContainerElement(element: GraphElementType) {
  return _LINEAR_CONTAINER_TYPES.includes(element[_TYPE_HEADER]);
}
export function isPairContainerElement(element: GraphElementType) {
  return _PAIR_CONTAINER_TYPES.includes(element[_TYPE_HEADER]);
}
export function isInitElement(element: GraphElementType) {
  return element[_TYPE_HEADER] === _INIT_TYPE_STRING;
}
export function isReferenceElement(element: GraphElementType) {
  return element[_TYPE_HEADER] === _REFERENCE_TYPE_STRING;
}

const _IDENTITY_STRING_SEPARATOR = '\u200b@';

export function revertNameCombo(nameCombo: string) {
  const components = nameCombo.split(_IDENTITY_STRING_SEPARATOR);
  return components[components.length - 1];
}

export function nameComboToClassName(nameCombo: string) {
  console.log(nameCombo);
  return nameCombo.split(_IDENTITY_STRING_SEPARATOR).join('_');
}
