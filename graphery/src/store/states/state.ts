export interface RootState {
  drawer: boolean;
}

export interface MetaState {
  siteName: string;
  navigationButtons: { name: string; icon: string }[];
  siteLogo: string;
  footerHTML: string;
}

export interface NotificationState {
  status: string;
  message: string;
  details: string;
}

export interface TutorialState {
  article: string;
  graphs: {
    [id: string]: { name: string; cyjs: object | string; info: string };
  } | null;
  codes: { [id: string]: { graphId: string; codes: string } } | null;
}
