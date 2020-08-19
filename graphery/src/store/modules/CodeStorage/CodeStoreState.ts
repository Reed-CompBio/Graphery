import {
  DateTimeMixinType,
  UniqueIdMixinType,
  IsPublishedMixinType,
} from '@/store/states/state';
import { ResultJsonTypeFromQueryData } from '@/store/modules/ResultJsonStorage/ResultJsonStoreState';

export interface CodeType extends UniqueIdMixinType {
  code?: string;
}

export interface CodeStoreType {
  codeObjectList: CodeType[] | null;
  currentCodeId: string | null;
}

export interface CodeTypeFromQueryData
  extends CodeType,
    DateTimeMixinType,
    IsPublishedMixinType {
  tutorial?: object;
  execresultjsonSet?: ResultJsonTypeFromQueryData[];
}
