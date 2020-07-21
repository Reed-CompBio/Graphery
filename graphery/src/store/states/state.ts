import { date } from 'quasar';

export interface RootState {
  drawer: boolean;
}

export interface MetaState {
  siteName: string;
  navigationButtons: { name: string; icon: string }[];
  siteLogo: string;
  headerSize: 66;
  footerHTML: string;
}

export const enum NotificationStatus {
  success = 'success',
  info = 'info',
  warning = 'warning',
  error = 'error',
  empty = '',
}

export interface NotificationState {
  status: NotificationStatus;
  message: string;
  details: string;
}

export interface Graph {
  id: string;
  isPublished: boolean;
  content: {
    title: string;
    abstract: string;
    isPublished: boolean;
  };
  priority: number;
  cyjs: object | string;
}

export interface ResultJsonType {
  json: string;
  graphId: string;
}

export interface TutorialMetaState {
  articleId: string | null;
  isAnchorPublished: boolean;
  isTransPublished: boolean;
  authors: string[];
  categories: string[];
  modifiedTime: string;
}

export interface TutorialArticleContent {
  title: string;
  contentHtml: string;
}

export interface TutorialState {
  metaState: TutorialMetaState | null;
  articleContent: TutorialArticleContent | null;
  // use v-for to spread graphs and make :key bind to id (or serial code?)
  currentGraphId: string | null;
  graphs: Graph[] | null;
  codes: string | null;
  resultJsonList: ResultJsonType[] | null;
  variableObj: object | null;
  customJson: object | null;
}

export interface TutorialContent {
  title: string;
  authors: string[];
  contentHtml: string;
  isPublished: boolean;
  modifiedTime: string;
}

export interface TutorialGraph {
  id: string;
  isPublished: boolean;
  content: {
    title: string;
    abstract: string;
    isPublished: boolean;
  };
  priority: number;
  cyjs: string;
}

export interface TutorialExecResultJson {
  json: string;
  graph: { id: string };
}

export interface TutorialCode {
  code: string;
  execresultjsonSet: TutorialExecResultJson[];
}

export interface TutorialDetailResponse {
  id: string;
  isPublished: boolean;
  categories: string[];
  content: TutorialContent;
  graphSet: TutorialGraph[];
  code: TutorialCode;
}

export const enum GraphLayoutEngines {
  dagre = 'dagre',
  hierarchical = 'hac',
}

export interface TutorialRequestState {
  articleUrl?: string;
  isPublished?: boolean;
  articleContent?: {
    title: string;
    contentHtml: string;
    authors: string[];
    categories: string[];
    modifiedTime: string;
    isPublished: boolean;
  } | null;
  // use v-for to spread graphs and make :key bind to id (or serial code?)
  graphs?: Graph[] | null;
  codes?: { [id: string]: { graphId: string; codes: string } } | null;
  resultJson?: string | null;
  variableObj?: object | null;
}

export interface SettingInfos {
  // color
  dark: boolean;
  graphDark: boolean;

  // graph render
  hideEdgeWhenRendering: boolean;
  renderViewportOnly: boolean;
  motionBlurEnabled: boolean;
  motionSensitivityLevel: number;
  graphSplitPos: number;
  // TODO maybe add a motion sensitivity?

  // editor settings
  enableEditing: boolean;
  tabNum: number;
  softTab: boolean;
  fontSize: number;
  codeWrap: boolean;

  // display
  pageDisplayNum: number;
  language: string;
  tooltips: boolean;
}

export interface SettingState extends SettingInfos {
  settingVer: '1.0.0';
}

export interface BaseState {
  drawer: boolean;
  csrfToken: string | null;
}

export interface CodeHistoryState {
  code: string;
  execResult: string;
}

export interface CodeHistoryCollectionState {
  [key: string]: CodeHistoryState;
}

export interface WorkSpaceInstance {
  name: string;
  code: string;
  lastModified: Date;
  execHistories: CodeHistoryCollectionState;
  // add a `from` field
}

export interface WorkSpaceBaseState {
  workspaces: WorkSpaceInstance[];
}
//
// export interface TutorialWorkSpaceState extends WorkSpaceBaseState {}
//
// export interface PlaygroundWorkSpace extends WorkSpaceBaseState {}

export interface WorkSpaceState {
  tutorialSpace: WorkSpaceBaseState;
  playgroundSpace: WorkSpaceBaseState;
}
