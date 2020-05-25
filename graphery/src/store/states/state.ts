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

export interface TutorialState {
  articleId: string | null;
  article: {
    title: string;
    content: string;
    authors: string[];
    categories: string[];
    time: string;
  } | null;
  graphIDs: string[] | null;
  // use v-for to spread graphs and make :key bind to id (or serial code?)
  graphs:
    | { id: string; name: string; cyjs: object | string; info: string }[]
    | null;
  codes: { [id: string]: { graphId: string; codes: string } } | null;
}

export interface TutorialRequestState {
  articleId?: string;
  article?: {
    title: string;
    content: string;
    authors: string[];
    categories: string[];
    time: string;
  } | null;
  graphIDs?: string[] | null;
  // use v-for to spread graphs and make :key bind to id (or serial code?)
  graphs?:
    | { id: string; name: string; cyjs: object | string; info: string }[]
    | null;
  codes?: { [id: string]: { graphId: string; codes: string } } | null;
}

export interface SettingState {
  dark: boolean;
  graphSplitPos: number;
  graphDark: boolean;
  hideEdgeWhenRendering: boolean;
  renderViewportOnly: boolean;
  motionBlurEnabled: boolean;
  motionSensitivityLevel: number;
}
