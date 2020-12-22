export interface VariableType {
  type: string;
  repr: string;
  id?: string;
  color?: string;
  properties?: object;
}

export interface VariableStoreType {
  currentVariables: VariableType[] | null;
}
