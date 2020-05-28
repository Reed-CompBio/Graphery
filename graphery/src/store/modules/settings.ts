import { RootState, SettingState } from '@/store/states/state';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

// TODO remove this and use web storage instead
const state: SettingState = {
  // color
  dark: false,
  graphDark: false,

  // graph render
  hideEdgeWhenRendering: false,
  renderViewportOnly: false,
  motionBlurEnabled: true,
  motionSensitivityLevel: 1,
  graphSplitPos: 50,

  // editor settings
  tabNum: 4,
  softTab: false,
  fontSize: 14,
  wrap: false,

  //
  pageDisplayNum: 5,
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
