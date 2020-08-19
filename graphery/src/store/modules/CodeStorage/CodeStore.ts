import { RootState } from '@/store/states/state';

import {
  CodeStoreType,
  CodeType,
  CodeTypeFromQueryData,
} from './CodeStoreState';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

// TODO remove the pseudo content!
const state: CodeStoreType = {
  codeObjectList: null,
  currentCodeId: null,
  // use v-for to spread graphs and make :key bind to id (or serial code?)
};

const mutations: MutationTree<CodeStoreType> = {
  LOAD_CODE_LIST(state, value: CodeType[]) {
    state.codeObjectList = value;
  },
  LOAD_CURRENT_CODE_ID(state, value: string) {
    state.currentCodeId = value;
  },

  // clear states
  CLEAR_CODE_LIST(state) {
    state.codeObjectList = null;
  },
  CLEAR_CURRENT_CODE_ID(state) {
    state.currentCodeId = null;
  },
};

const actions: ActionTree<CodeStoreType, RootState> = {
  loadCodeListFromQueryData({ commit }, codeList: CodeTypeFromQueryData[]) {
    commit('LOAD_CODE_LIST', codeList);
  },
  loadCodeListFromMatched({ commit }, codeList: CodeType[]) {
    commit('LOAD_CODE_LIST', codeList);
  },
  loadCurrentCodeId({ commit }, codeId: string) {
    commit('LOAD_CURRENT_CODE_ID', codeId);
  },
  CLEAR_ALL({ commit }) {
    commit('CLEAR_CODE_LIST');
    commit('CLEAR_CURRENT_CODE_ID');
  },
};

const getters: GetterTree<CodeStoreType, RootState> = {
  getCurrentCodeId(state) {
    return state.currentCodeId;
  },
  codeObjectListEmpty(state) {
    return state.codeObjectList === null;
  },
  getCurrentCodeObject(state) {
    if (state.codeObjectList) {
      return state.codeObjectList.find((obj) => obj.id === state.currentCodeId);
    }
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
