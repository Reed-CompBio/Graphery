import {
  RootState,
  TutorialArticleContent,
  TutorialDetailResponse,
  TutorialMetaState,
  TutorialState,
} from '@/store/states/state';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

// TODO remove the pseudo content!
const state: TutorialState = {
  metaState: null,
  articleContent: null,
};

const mutations: MutationTree<TutorialState> = {
  LOAD_META_STATE(state, value: TutorialMetaState) {
    state.metaState = value;
  },
  LOAD_ARTICLE_CONTENT(state, value: TutorialArticleContent) {
    state.articleContent = value;
  },
  // clear states
  CLEAR_META_STATE(state) {
    state.metaState = null;
  },
  CLEAR_ARTICLE_CONTENT(state) {
    state.articleContent = null;
  },
};

const actions: ActionTree<TutorialState, RootState> = {
  loadTutorialMetaState({ commit }, metaState: TutorialMetaState) {
    commit('LOAD_META_STATE', metaState);
  },
  loadTutorialArticleContent(
    { commit },
    articleContent: TutorialArticleContent
  ) {
    commit('LOAD_ARTICLE_CONTENT', articleContent);
  },
  loadTutorial({ dispatch, commit }, tutorialObj: TutorialDetailResponse) {
    console.debug('received tutorial detail obj', tutorialObj);

    // Load metadata
    dispatch('loadTutorialMetaState', {
      articleId: tutorialObj.id,
      isAnchorPublished: tutorialObj.isPublished,
      isTransPublished: tutorialObj.content.isPublished,
      authors: tutorialObj.content.authors.map((obj) => obj.username),
      categories: tutorialObj.categories.map((obj) => obj.category),
      modifiedTime: tutorialObj.content.modifiedTime,
    });

    // load article content
    dispatch('loadTutorialArticleContent', {
      title: tutorialObj.content.title,
      contentHtml: tutorialObj.content.contentHtml,
    });
  },
  clearAll({ commit }) {
    commit('CLEAR_META_STATE');
    commit('CLEAR_ARTICLE_CONTENT');
  },
};

const getters: GetterTree<TutorialState, RootState> = {
  title(state) {
    return state.articleContent && state.articleContent.title;
    // return state.articleContent ? state.articleContent.title : null;
  },
  htmlContent(state) {
    return state.articleContent && state.articleContent.contentHtml;
    // return state.articleContent ? state.articleContent.content : null;
  },
  authors(state) {
    return state.metaState && state.metaState.authors;
  },
  categories(state) {
    return state.metaState && state.metaState.categories;
  },
  articleModTime(state) {
    return state.metaState && state.metaState.modifiedTime;
  },
  articleEmpty(state) {
    return state.articleContent === null;
  },
  isAnchorPublished(state) {
    return state.metaState && state.metaState.isAnchorPublished;
  },
  isTransPublished(state) {
    return state.metaState && state.metaState.isTransPublished;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
