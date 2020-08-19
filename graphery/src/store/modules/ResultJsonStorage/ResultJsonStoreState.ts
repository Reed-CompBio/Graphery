export interface ResultJsonType {
  json: string;
  graphId: string;
  codeId: string;
}

export interface ResultJsonTypeFromQueryData {
  json: string;
  code: {
    id: string;
  };
  graph: {
    id: string;
  };
}

export interface ResultJsonStateType {
  resultJsonStringList: ResultJsonType[] | null;
  currentResultJsonString: string | null;
  currentResultJsonObject: object | null;
}
