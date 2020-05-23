export interface RootState {
  drawer: boolean;
}

export interface MetaState {
  siteName: string;
  navigationButtons: { name: string; icon: string }[];
  siteLogo: string;
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

export interface TutorialInfoState {
  articleId: string;
  article: { title: string; content: string } | null;
  graphIDs: string[] | null;
  // use v-for to spread graphs and make :key bind to id (or serial code?)
  graphs:
    | { id: string; name: string; cyjs: object | string; info: string }[]
    | null;
  codes: { [id: string]: { graphId: string; codes: string } } | null;
}

export interface TutorialRequestState {
  time: string;
  articleId?: string;
  article?: { title: string; content: string } | null;
  graphIDs?: string[] | null;
  // use v-for to spread graphs and make :key bind to id (or serial code?)
  graphs?:
    | { id: string; name: string; cyjs: object | string; info: string }[]
    | null;
  codes?: { [id: string]: { graphId: string; codes: string } } | null;
}

export interface TutorialState {
  tutorials: { [time: string]: TutorialInfoState };
}

export interface SettingState {
  dark: boolean;
  graphDark: boolean;
  hideEdgeWhenRendering: boolean;
  renderViewportOnly: boolean;
  motionBlurEnabled: boolean;
  motionSensitivityLevel: number;
}
