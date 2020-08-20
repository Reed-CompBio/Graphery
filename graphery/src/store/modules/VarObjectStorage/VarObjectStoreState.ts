export interface VariableType {
  type: string;
  repr: string;
  id?: string;
  color?: string;
}

export interface VariableStoreType {
  currentVariables: VariableType[] | null;
}
