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
