export interface PriorityType {
  id?: string;
  priority?: number;
  label?: string;
}

export interface GraphInfoContentType {
  title?: string;
  abstract?: string;
  isPublished?: boolean;
}

export interface GraphType {
  id?: string;
  isPublished?: boolean;
  content?: GraphInfoContentType;
  priority?: PriorityType;
  cyjs?: string;
}

export interface GraphStoreType {
  graphs: GraphType[] | null;
  currentGraphId: string | null;
  currentGraphJsonString: string | null;
}

export interface GraphTypeFromQueryData extends GraphType {
  createdTime?: Date;
  modifiedTime?: Date;
  url?: string;
  name?: string;
  categories?: [];
  tutorials?: [];
  execresultjsonSet?: [];
  authors?: [];
}
