import { GraphTypeFromQueryData } from '@/store/modules/GraphStorage/GraphStoreState';
import { CodeTypeFromQueryData } from '@/store/modules/CodeStorage/CodeStoreState';

export interface ResultJsonType {
  json: string;
  graphId: string;
  codeId: string;
}

export interface ResultJsonTypeFromQueryData {
  json: string;
  code: CodeTypeFromQueryData;
  graph: GraphTypeFromQueryData;
}

export interface ResultJsonStateType {
  resultJsonStringList: ResultJsonType[] | null;
  currentResultJsonString: string | null;
  currentResultJsonObject: object | null;
}
