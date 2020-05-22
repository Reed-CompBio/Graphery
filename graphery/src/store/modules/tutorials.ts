import { TutorialState, RootState } from '@/store/states/state';
import { MutationTree, ActionTree, Action, GetterTree } from 'vuex';

const state: TutorialState = {
  // TODO do I need the ids?
  articleId: null,
  article: null,
  graphIDs: null,
  graphs: null,
  codes: null,
};

const mutations: MutationTree<TutorialState> = {
  LOAD_ARTICLE_ID(state, value) {
    state.articleId = value;
  },
  LOAD_ARTICLES(state, value) {
    state.article = value;
  },
  LOAD_GRAPH_IDS(state, value) {
    state.graphIDs = value;
  },
  LOAD_GRAPHS(state, value) {
    state.graphs = value;
  },
  LOAD_CODES(state, value) {
    state.codes = value;
  },
  // don't know how to write this
  // MODIFY_GRAPH_BY_ID(state, info) {},
};

const actions: ActionTree<TutorialState, RootState> = {
  loadTutorial({ commit }, tutorialId) {
    let article;
    let graphIds;
    // TODO promises
    commit('LOAD_ARTICLES', article);
    commit('LOAD_GRAPH_IDS', graphIds);
  },
  loadGraphsByIds({ commit }, graphIds) {
    let graphs;
    // TODO promises
    commit('LOAD_GRAPHS', graphs);
  },
  loadCodes({ commit }, graphIds) {
    let codes;
    // TODO promises
    commit('LOAD_CODES', codes);
  },
  clearAll({ commit }) {
    commit('LOAD_ARTICLE_ID', null);
    commit('LOAD_ARTICLES', null);
    commit('LOAD_GRAPH_IDS', null);
    commit('LOAD_GRAPHS', null);
    commit('LOAD_CODES', null);
  },
  // don't know how to write this
  // modifyGraphById({ commit, getters }, { graphId, delta }) {},
};

const getters: GetterTree<TutorialState, RootState> = {
  articleEmpty(state) {
    return state.article === null;
  },
  graphsEmpty(state) {
    return state.graphs === null;
  },
  codesEmpty(state) {
    return state.codes === null;
  },
  getGraphById: (state) => (id: string) => {
    return state.graphs ? state.graphs.find((graph) => graph.id == id) : null;
  },
  getGraphByIndex: (state) => (index: number) => {
    return state.graphs ? state.graphs[index] : null;
  },
  getCodeById: (state) => (id: string) => {
    return state.codes ? state.codes[id] : null;
  },
  getCodeByIndex: (state) => (index: number) => {
    return state.codes ? state.codes[index] : null;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
