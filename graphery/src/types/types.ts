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

export interface AllTutorialContentType {
  title: string;
  authors: string[];
  abstract: string[];
  isPublished: boolean;
  modifiedTime: string;
}

export interface AllTutorialInfoType {
  url: string;
  isPublished: boolean;
  categories: string[];
  content: AllTutorialContentType;
}

export interface AllTutorialDataType {
  allTutorialInfo: AllTutorialInfoType[];
}
