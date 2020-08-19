import { RootState } from '@/store/states/state';

import {
  ResultJsonType,
  ResultJsonStateType,
  ResultJsonTypeFromQueryData,
} from './ResultJsonStoreState';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

// TODO remove the pseudo content!
const state: ResultJsonStateType = {
  resultJsonStringList: null,
  currentResultJsonString: null,
  currentResultJsonObject: null,
  // use v-for to spread graphs and make :key bind to id (or serial code?)
};

const mutations: MutationTree<ResultJsonStateType> = {
  LOAD_RESULT_JSON_STRING_LIST(state, value: ResultJsonType[]) {
    state.resultJsonStringList = value;
  },
  LOAD_CURRENT_RESULT_JSON_STRING(state, value: string) {
    state.currentResultJsonString = value;
  },
  LOAD_CURRENT_RESULT_JSON_OBJECT(state, value: object) {
    state.currentResultJsonObject = value;
  },

  // clear states
  CLEAR_RESULT_JSON_STRING_LIST(state) {
    state.resultJsonStringList = null;
  },
  CLEAR_CURRENT_RESULT_JSON_STRING(state) {
    state.currentResultJsonString = null;
  },
  CLEAR_CURRENT_RESULT_JSON_OBJECT(state) {
    state.currentResultJsonObject = null;
  },
};

const actions: ActionTree<ResultJsonStateType, RootState> = {
  loadResultJsonListFromQueryData(
    { commit },
    resultJsonSet: ResultJsonTypeFromQueryData[]
  ) {
    const resultJsonStringList = resultJsonSet.map((obj) => {
      return {
        json: obj.json,
        graphId: obj.graph.id,
        codeId: obj.code.id,
      };
    });

    commit('LOAD_RESULT_JSON_STRING_LIST', resultJsonStringList);
  },
  loadResultJsonListFromMatched({ commit }, resultJsonSet: ResultJsonType[]) {
    commit('LOAD_RESULT_JSON_STRING_LIST', resultJsonSet);
  },
  loadCurrentJsonString({ commit }, resultJsonString: string) {
    commit('LOAD_CURRENT_RESULT_JSON_STRING', resultJsonString);
  },
  loadCurrentJsonObject({ commit }, resultJsonObj: object) {
    commit('LOAD_CURRENT_RESULT_JSON_OBJECT', resultJsonObj);
  },
  CLEAR_ALL({ commit }) {
    commit('CLEAR_RESULT_JSON_STRING_LIST');
    commit('CLEAR_CURRENT_RESULT_JSON_STRING');
    commit('CLEAR_CURRENT_RESULT_JSON_OBJECT');
  },
};

const getters: GetterTree<ResultJsonStateType, RootState> = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
