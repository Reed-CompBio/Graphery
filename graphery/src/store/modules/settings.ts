import { RootState, SettingState } from '@/store/states/state';
import { GetterTree } from 'vuex';

const state: SettingState = {
  dark: true,
  graphSplitPos: 50,
  graphDark: false,
  hideEdgeWhenRendering: false,
  renderViewportOnly: false,
  motionBlurEnabled: true,
  motionSensitivityLevel: 1,
};

const getters: GetterTree<SettingState, RootState> = {
  graphBackgroundColor(state) {
    return state.graphDark ? '#1D1D1D' : '#ffffff';
  },
};

export default {
  namespaced: true,
  state,
  getters,
};
