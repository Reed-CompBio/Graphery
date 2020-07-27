import {
  Graph,
  ResultJsonType,
  RootState,
  TutorialArticleContent,
  TutorialDetailResponse,
  TutorialGraph,
  TutorialMetaState,
  TutorialState,
} from '@/store/states/state';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

// TODO remove the pseudo content!
const state: TutorialState = {
  metaState: null,
  articleContent: null,
  currentGraphId: null,
  currentCodeId: null,
  graphs: null,
  codes: null,
  resultJsonList: null,
  variableObj: null,
  customJson: null,
  // use v-for to spread graphs and make :key bind to id (or serial code?)
};

const mutations: MutationTree<TutorialState> = {
  LOAD_META_STATE(state, value: TutorialMetaState) {
    state.metaState = value;
  },
  LOAD_ARTICLE_CONTENT(state, value: TutorialArticleContent) {
    state.articleContent = value;
  },
  LOAD_CURRENT_GRAPH_ID(state, value: string) {
    state.currentGraphId = value;
  },
  LOAD_CURRENT_CODE_ID(state, value: string) {
    state.currentCodeId = value;
  },
  LOAD_GRAPHS(state, value: TutorialGraph[]) {
    state.graphs = value;
  },
  LOAD_CODES(state, value: string) {
    state.codes = value;
  },
  LOAD_RESULT_JSON_LIST(state, value: ResultJsonType[]) {
    state.resultJsonList = value;
  },
  LOAD_VARIABLE_OBJ(state, obj) {
    state.variableObj = obj;
  },
  LOAD_CUSTOM_JSON(state, obj) {
    state.customJson = obj;
  },

  // clear states
  CLEAR_META_STATE(state) {
    state.metaState = null;
  },
  CLEAR_ARTICLE_CONTENT(state) {
    state.articleContent = null;
  },
  CLEAR_CURRENT_GRAPH_ID(state) {
    state.currentGraphId = null;
  },
  CLEAR_GRAPHS(state) {
    state.graphs = null;
  },
  CLEAR_CODES(state) {
    state.codes = null;
  },
  CLEAR_RESULT_JSON_LIST(state) {
    state.resultJsonList = null;
  },
  CLEAR_VARIABLE_OBJ(state) {
    state.variableObj = null;
  },
  CLEAR_CUSTOM_JSON(state) {
    state.variableObj = null;
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
  loadTutorialGraphs({ commit }, graphs: Graph[]) {
    commit('LOAD_GRAPHS', graphs);
  },
  loadTutorialCode({ commit }, code: string) {
    commit('LOAD_CODES', code);
  },
  loadTutorialResultJsonList({ commit }, resultJsonList: ResultJsonType[]) {
    commit('LOAD_RESULT_JSON_LIST', resultJsonList);
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

    // load tutorial graphs
    dispatch('loadTutorialGraphs', tutorialObj.graphSet);

    // load tutorial code
    dispatch('loadTutorialCode', tutorialObj.code.code);

    // load current code id
    commit('LOAD_CURRENT_CODE_ID', tutorialObj.code.id);

    // load execution result json
    const resultJsonList: ResultJsonType[] = [];
    tutorialObj.code.execresultjsonSet.forEach((resultJsonObj) => {
      resultJsonList.push({
        json: resultJsonObj.json,
        graphId: resultJsonObj.graph.id,
        codeId: tutorialObj.code.id,
      });
    });
    dispatch('loadTutorialResultJsonList', resultJsonList);
  },
  loadVariableObj({ commit }, list) {
    commit('LOAD_VARIABLE_OBJ', list);
  },
  loadCustomJson({ commit }, list) {
    commit('LOAD_CUSTOM_JSON', list);
  },
  clearAll({ commit }) {
    commit('CLEAR_META_STATE');
    commit('CLEAR_ARTICLE_CONTENT');
    commit('CLEAR_CURRENT_GRAPH_ID');
    commit('CLEAR_GRAPHS');
    commit('CLEAR_CODES');
    commit('CLEAR_RESULT_JSON_LIST');
    commit('CLEAR_VARIABLE_OBJ');
    commit('CLEAR_CUSTOM_JSON');
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
  graphsEmpty(state) {
    return state.graphs === null;
  },
  codesEmpty(state) {
    return state.codes === null;
  },
  resultJsonArrEmpty(state, getter) {
    return getter.resultJsonArr.length === 0;
  },
  resultJsonArr(state, getter) {
    if (state.customJson !== null) {
      return state.customJson;
    }

    if (getter.resultJson === null) {
      return [];
    }

    return JSON.parse(getter.resultJson);
  },
  variableObjEmpty(state, getter) {
    return (
      getter.codesEmpty || getter.graphsEmpty || state.variableObj === null
    );
  },
  getGraphList(state) {
    return state.graphs;
  },
  resultJson(state) {
    if (state.resultJsonList) {
      const resultJsonObj = state.resultJsonList.find(
        (r) =>
          r.graphId === state.currentGraphId && r.codeId === state.currentCodeId
      );
      if (resultJsonObj) {
        return resultJsonObj.json;
      }
    }

    return null;
  },
  getGraphById: (state) => (id: string) => {
    // TODO may return undefined
    return state.graphs && state.graphs.find((g) => g.id === id);
  },
  getGraphByIndex: (state) => (index: number) => {
    return state.graphs && state.graphs[index];
  },
  currentGraph(state, getter) {
    return getter.getGraphById(state.currentGraphId) || null;
  },
  currentGraphJsonObj(state, getter) {
    if (getter.currentGraph && getter.currentGraph.cyjs) {
      // which should always happen since the graphs are chosen by ids which corresponds
      // defined graphs
      return JSON.parse(getter.currentGraph.cyjs);
    }
    return null;
  },
  currentGraphContent(state, getter) {
    if (getter.currentGraph && getter.currentGraph.content) {
      return getter.currentGraph.content;
    }
    return null;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
