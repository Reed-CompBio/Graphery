import { RankType } from '@/types/types';

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

export interface AuthorState {
  username?: string;
  firstName?: string;
  lastName?: string;
}

export interface TutorialMetaState {
  articleId: string | null;
  isAnchorPublished: boolean;
  isTransPublished: boolean;
  rank: RankType;
  authors: AuthorState[];
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
}

export interface UserType {
  username?: string;
  email?: string;
  role?: string;
  firstName?: string;
  lastName?: string;
}

export interface TutorialContent {
  title: string;
  authors: UserType[];
  contentHtml: string;
  isPublished: boolean;
  modifiedTime: string;
}

export interface CategoryType {
  id: string;
  category: string;
}

export interface TutorialDetailResponse {
  id: string;
  isPublished: boolean;
  rank: RankType;
  categories: CategoryType[];
  content: TutorialContent;
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
  variableListHorizontal: boolean;

  // display
  pageDisplayNum: number;
  language: string;
  tooltips: boolean;
  graphAbstractPopupShow: boolean;

  // invisible state
  tosAgreeAndDoNotShowAgain: boolean;
  tosVersion: string | null;

  // intro state
  showIntro: {
    tutorialIntro: boolean;
    graphIntro: boolean;
  };
}

export interface SettingState extends SettingInfos {
  settingVer: '1.0.0';
}

export interface BaseState {
  drawer: boolean;
  csrfToken: string | null;
  user: UserType | null;
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

export interface ContentStoreType {
  [key: string]: {
    raw: string;
    rendered: string;
  };
}

export interface EditState {
  content: {
    tutorialContent: ContentStoreType;
    graphInfoContent: ContentStoreType;
  };
}

export interface ContentRequestType {
  contentId: string;
  content: { raw: string; rendered: string };
}

export interface DateTimeMixinType {
  createdTime?: string;
  modifiedTime?: string;
}

export interface IsPublishedMixinType {
  isPublished?: boolean;
}

export interface UniqueIdMixinType {
  id?: string;
}
