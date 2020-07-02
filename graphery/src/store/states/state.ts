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
  name: string;
  cyjs: object | string;
  layoutEngine: GraphLayoutEngines;
  info: string;
}

export interface TutorialState {
  articleUrl: string | null;
  isPublished: boolean | null;
  articleContent: {
    title: string;
    contentHtml: string;
    // Meta data
    authors: string[];
    categories: string[];
    modifiedTime: string;
    isPublished: boolean;
  } | null;
  // use v-for to spread graphs and make :key bind to id (or serial code?)
  currentGraphId: string | null;
  graphs: Graph[] | null;
  codes: { [id: string]: { graphId: string; codes: string } } | null;
  resultJson: string | null;
  variableObj: object | null;
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
