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
  info: boolean;
  warning: boolean;
  error: boolean;
  message: string;
  details: string;
}
