import {
  DateTimeMixinType,
  UniqueIdMixinType,
  IsPublishedMixinType,
} from '@/store/states/state';
import { ResultJsonTypeFromQueryData } from '@/store/modules/ResultJsonStorage/ResultJsonStoreState';

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

export interface GraphType extends IsPublishedMixinType, UniqueIdMixinType {
  content?: GraphInfoContentType;
  priority?: PriorityType;
  cyjs?: string;
}

export interface GraphStoreType {
  graphObjectList: GraphType[] | null;
  currentGraphId: string | null;
  currentGraphJsonString: string | null;
}

export interface GraphTypeFromQueryData extends GraphType, DateTimeMixinType {
  url?: string;
  name?: string;
  categories?: [];
  tutorials?: [];
  execresultjsonSet?: ResultJsonTypeFromQueryData[];
  authors?: [];
}
