import { RootState } from '@/store/states/state';

import { VariableStoreType, VariableType } from './VarObjectStoreState';
import { ActionTree, GetterTree, MutationTree } from 'vuex';
import { VARIABLE_EMPTY_CONTENT_NOTATION } from '@/components/framework/GraphEditorControls/parameters';

const state: VariableStoreType = {
  currentVariables: null,
  currentAccessedVariables: null,
};

const mutations: MutationTree<VariableStoreType> = {
  LOAD_CURRENT_VARIABLES(state, value: VariableType[]) {
    state.currentVariables = value;
  },
  // clear states
  CLEAR_CURRENT_VARIABLES(state) {
    state.currentVariables = null;
  },
  LOAD_CURRENT_ACCESSES(state, value: VariableType[]) {
    state.currentAccessedVariables = value;
  },
  CLEAR_CURRENT_ACCESSES(state) {
    state.currentAccessedVariables = null;
  },
};

const actions: ActionTree<VariableStoreType, RootState> = {
  loadCurrentVariables({ commit }, variables: VariableType[]) {
    commit('LOAD_CURRENT_VARIABLES', variables);
  },
  loadCurrentAccesses({ commit }, variables: VariableType[]) {
    commit('LOAD_CURRENT_ACCESSES', variables);
  },
  CLEAR_ALL({ commit }) {
    commit('CLEAR_CURRENT_VARIABLES');
    commit('CLEAR_CURRENT_ACCESSES');
  },
};

const getters: GetterTree<VariableStoreType, RootState> = {
  getCurrentVariables(state) {
    return state.currentVariables;
  },
  currentVariablesEmpty(state) {
    return state.currentVariables === VARIABLE_EMPTY_CONTENT_NOTATION;
  },
  getCurrentAccessedVariables(state) {
    return state.currentAccessedVariables;
  },
  currentAccessedVariableEmpty(state) {
    return !(
      state.currentAccessedVariables && state.currentAccessedVariables.length
    );
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
