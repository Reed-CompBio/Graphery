import { GraphTypeFromQueryData } from '@/store/modules/GraphStorage/GraphStoreState';
import { CodeTypeFromQueryData } from '@/store/modules/CodeStorage/CodeStoreState';

export interface KeysType {
  graphId: string;
  codeId: string;
}

export interface ResultJsonType extends KeysType {
  json: string;
}

export interface ResultJsonInterface {
  label: string;
  type: string;
  color: string;
  python_id: string;
  properties?: object;
  id?: string;
}

interface VariableListColorType {
  [variableIdentifier: string]: string;
}

export interface ResultJsonObjectType extends KeysType {
  jsonObject: ResultJsonInterface[];
  colorList: VariableListColorType;
}

export interface ResultJsonTypeFromQueryData {
  json: string;
  code: CodeTypeFromQueryData;
  graph: GraphTypeFromQueryData;
}

export interface VariableListInfoType {
  variableHighlightToggle: {
    [varName: string]: number;
  };
  variableListOrder: string[];
}

export interface PositionType {
  [key: string]: {
    position: number;
    variableListInfo: VariableListInfoType;
  };
}

export interface ResultJsonStateType {
  resultJsonStringList: ResultJsonType[] | null;
  resultJsonObjectList: ResultJsonObjectType[] | null;
  resultJsonPositions: PositionType;
}
