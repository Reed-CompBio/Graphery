import {
  GRAPH_ELEMENT_TYPE,
  NORMAL_VARIABLE_TYPE,
} from '@/components/framework/GraphEditorControls/parameters';

export interface TypedVariableObject {
  type: string;
}

export function isGraphElement(value: TypedVariableObject | null) {
  return value && value.type === GRAPH_ELEMENT_TYPE;
}

export function isNormalElement(value: TypedVariableObject | null) {
  return value && value.type === NORMAL_VARIABLE_TYPE;
}

export function revertNameCombo(nameCombo: string) {
  return nameCombo.split('#')[1];
}
