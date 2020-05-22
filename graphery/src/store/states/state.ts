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
  articleId: string | null;
  article: { title: string; content: string } | null;
  graphIDs: string[] | null;
  // use v-for to spread graphs and make :key bind to id (or serial code?)
  graphs:
    | { id: string; name: string; cyjs: object | string; info: string }[]
    | null;
  codes: { [id: string]: { graphId: string; codes: string } } | null;
}
