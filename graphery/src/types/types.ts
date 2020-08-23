export interface ArticleDisplayInfoType {
  url: string;
  categories: string[];
  isAnchorPublished: boolean;
  title: string;
  authors: string[];
  modifiedTime: string;
  abstract: string;
  isTransPublished: boolean;
}

export interface TutorialAbstractContentType {
  title: string;
  authors: string[];
  abstract: string[];
  isPublished: boolean;
  modifiedTime: string;
}

export interface RankType {
  level: number;
  section: number;
}

export interface AllTutorialsInfoType {
  url: string;
  isPublished: boolean;
  rank: RankType;
  categories: string[];
  content: TutorialAbstractContentType;
}

export interface AllTutorialDataType {
  allTutorialInfo: AllTutorialsInfoType[];
}

export interface LocalServerSuccessResponse {
  data: {
    codeHash: string;
    execResult: [];
  };
}
