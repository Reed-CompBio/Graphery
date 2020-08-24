import { RootState } from '@/store/states/state';

import {
  GraphStoreType,
  GraphType,
  GraphTypeFromQueryData,
} from './GraphStoreState';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

const state: GraphStoreType = {
  graphObjectList: null,
  currentGraphId: null,
};

const mutations: MutationTree<GraphStoreType> = {
  LOAD_GRAPH_OBJECT_LIST(state, value: GraphType[]) {
    state.graphObjectList = value;
  },
  LOAD_CURRENT_GRAPH_ID(state, value: string) {
    state.currentGraphId = value;
  },

  // clear states
  CLEAR_GRAPHS(state) {
    state.graphObjectList = null;
  },
  CLEAR_CURRENT_GRAPH_ID(state) {
    state.currentGraphId = null;
  },
};

const actions: ActionTree<GraphStoreType, RootState> = {
  loadGraphListFromQueryData({ commit }, graphList: GraphTypeFromQueryData[]) {
    commit('LOAD_GRAPH_OBJECT_LIST', graphList);
  },
  loadGraphListFromMatched({ commit }, graphList: GraphType[]) {
    commit('LOAD_GRAPH_OBJECT_LIST', graphList);
  },
  loadCurrentGraphId({ commit }, graphId: string) {
    commit('LOAD_CURRENT_GRAPH_ID', graphId);
  },
  CLEAR_ALL({ commit }) {
    commit('CLEAR_GRAPHS');
    commit('CLEAR_CURRENT_GRAPH_ID');
  },
};

const getters: GetterTree<GraphStoreType, RootState> = {
  getCurrentGraphId(state) {
    return state.currentGraphId;
  },
  graphObjectListEmpty(state) {
    return state.graphObjectList === null;
  },
  getGraphObjectList(state) {
    return state.graphObjectList;
  },
  getCurrentGraphObject(state, getter) {
    return getter.getGraphObjectById(state.currentGraphId) || null;
  },
  getCurrentGraphObjectTitle(state, getter) {
    return (
      getter.getCurrentGraphObject && getter.getCurrentGraphObject.content.title
    );
  },
  getGraphObjectById: (state) => (id: string) => {
    // TODO may return undefined
    return (
      state.graphObjectList && state.graphObjectList.find((g) => g.id === id)
    );
  },
  getGraphObjectByIndex: (state) => (index: number) => {
    return state.graphObjectList && state.graphObjectList[index];
  },
  autoGeneratedCurrentGraphObject(state, getter) {
    return getter.getGraphObjectById(state.currentGraphId) || null;
  },
  autoGeneratedCurrentGraphObjectIsPublished(state, getter) {
    return (
      getter.autoGeneratedCurrentGraphObject &&
      getter.autoGeneratedCurrentGraphObject.isPublished
    );
  },
  autoGeneratedCurrentGraphObjectContent(state, getter) {
    return (
      getter.autoGeneratedCurrentGraphObject &&
      getter.autoGeneratedCurrentGraphObject.content
    );
  },
  autoGeneratedCurrentGraphObjectTitle(state, getter) {
    return (
      getter.autoGeneratedCurrentGraphObjectContent &&
      getter.autoGeneratedCurrentGraphObjectContent.title
    );
  },

  autoGeneratedCurrentGraphObjectAbstractHtml(state, getter) {
    return (
      getter.autoGeneratedCurrentGraphObjectContent &&
      getter.autoGeneratedCurrentGraphObjectContent.abstract
    );
  },
  autoGeneratedCurrentGraphJsonString(state, getter) {
    const currentGraphObject = getter.autoGeneratedCurrentGraphObject;
    return currentGraphObject && currentGraphObject.cyjs;
  },
  autoGeneratedCurrentGraphJsonObj(state, getter) {
    const cyjs = getter.autoGeneratedCurrentGraphJsonString;
    // which should always happen since the graphs are chosen by ids which corresponds
    // defined graphs
    return cyjs && JSON.parse(cyjs);
  },
  autoGeneratedCurrentGraphContent(state, getter) {
    const currentGraphObject = getter.autoGeneratedCurrentGraphObject;
    if (currentGraphObject && currentGraphObject.content) {
      return currentGraphObject.content;
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
