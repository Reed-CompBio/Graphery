import { GraphTypeFromQueryData } from '@/store/modules/GraphStorage/GraphStoreState';
import { CodeTypeFromQueryData } from '@/store/modules/CodeStorage/CodeStoreState';

export interface KeysType {
  graphId: string;
  codeId: string;
}

export interface ResultJsonType extends KeysType {
  json: string;
}

export interface ResultJsonObjectType extends KeysType {
  jsonObject: object;
}

export interface ResultJsonTypeFromQueryData {
  json: string;
  code: CodeTypeFromQueryData;
  graph: GraphTypeFromQueryData;
}

export interface PositionType {
  [key: string]: { position: number };
}

export interface ResultJsonStateType {
  resultJsonStringList: ResultJsonType[] | null;
  resultJsonObjectList: ResultJsonObjectType[] | null;
  resultJsonPositions: PositionType;
}
