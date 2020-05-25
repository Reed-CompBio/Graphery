import { RootState, SettingState } from '@/store/states/state';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

const state: SettingState = {
  dark: true,
  graphSplitPos: 50,
  graphDark: false,
  hideEdgeWhenRendering: false,
  renderViewportOnly: false,
  motionBlurEnabled: true,
  motionSensitivityLevel: 1,
};

const mutations: MutationTree<SettingState> = {
  CHANGE_SEP_POS(state, value: number) {
    state.graphSplitPos = value;
  },
};

const actions: ActionTree<SettingState, RootState> = {
  changeSepPos({ commit }, value: number) {
    commit('CHANGE_SEP_POS', value);
  },
};

const getters: GetterTree<SettingState, RootState> = {
  graphBackgroundColor(state) {
    return state.graphDark ? '#1D1D1D' : '#ffffff';
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
