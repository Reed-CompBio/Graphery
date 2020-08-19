import { RootState } from '@/store/states/state';

import {
  GraphStoreType,
  GraphType,
  GraphTypeFromQueryData,
} from './GraphStoreState';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

// TODO remove the pseudo content!
const state: GraphStoreType = {
  graphs: null,
  currentGraphId: null,
  currentGraphJsonString: null,
  // use v-for to spread graphs and make :key bind to id (or serial code?)
};

const mutations: MutationTree<GraphStoreType> = {
  LOAD_GRAPHS(state, value: GraphType[]) {
    state.graphs = value;
  },
  LOAD_CURRENT_GRAPH_ID(state, value: string) {
    state.currentGraphId = value;
  },
  LOAD_CURRENT_GRAPH_JSON_STRING(state, value: string) {
    state.currentGraphJsonString = value;
  },

  // clear states
  CLEAR_GRAPHS(state) {
    state.graphs = null;
  },
  CLEAR_CURRENT_GRAPH_ID(state) {
    state.currentGraphId = null;
  },
  CLEAR_CURRENT_GRAPH_JSON_STRING(state) {
    state.currentGraphJsonString = null;
  },
};

const actions: ActionTree<GraphStoreType, RootState> = {
  loadGraphsFromQueryData({ commit }, graphs: GraphTypeFromQueryData[]) {
    commit('LOAD_GRAPHS', graphs);
  },
  loadGraphsFromMatched({ commit }, graphs: GraphType[]) {
    commit('LOAD_GRAPHS', graphs);
  },
  loadCurrentGraphJsonString({ commit }, graphJsonString: string) {
    commit('LOAD_CURRENT_GRAPH_JSON_STRING', graphJsonString);
  },
  loadCurrentGraphId({ commit }, graphId: object) {
    commit('LOAD_CURRENT_GRAPH_ID', graphId);
  },
  CLEAR_ALL({ commit }) {
    commit('CLEAR_GRAPHS');
    commit('CLEAR_CURRENT_GRAPH_ID');
    commit('CLEAR_CURRENT_GRAPH_JSON_STRING');
  },
};

const getters: GetterTree<GraphStoreType, RootState> = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
