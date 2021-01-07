import { RootState } from '@/store/states/state';

import {
  CodeStoreType,
  CodeType,
  CodeTypeFromQueryData,
} from './CodeStoreState';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

const state: CodeStoreType = {
  codeObjectList: null,
  currentCodeId: null,
};

const mutations: MutationTree<CodeStoreType> = {
  LOAD_CODE_LIST(state, value: CodeType[]) {
    state.codeObjectList = value;
  },
  LOAD_CURRENT_CODE_ID(state, value: string) {
    state.currentCodeId = value;
  },
  CHANGE_CODE_CONTENT(state, value: { codeObject: CodeType; code: string }) {
    value.codeObject.code = value.code;
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
  getCurrentCodeName(state, getters) {
    const currentCodeObj = getters.getCurrentCodeObject;
    if (currentCodeObj) {
      return currentCodeObj.name;
    }
    return '';
  },
  getCurrentCodeId(state) {
    return state.currentCodeId;
  },
  codeObjectListEmpty(state) {
    return state.codeObjectList === null;
  },
  getCodeList(state) {
    return state.codeObjectList;
  },
  getCurrentCodeObject(state) {
    if (state.codeObjectList) {
      return state.codeObjectList.find((obj) => obj.id === state.currentCodeId);
    }
    return null;
  },
  getCurrentCodeContent(state, getter) {
    return getter.getCurrentCodeObject && getter.getCurrentCodeObject.code;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
