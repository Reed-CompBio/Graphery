import { SettingState } from '@/store/states/state';

const state: SettingState = {
  dark: true,
  graphDark: false,
  hideEdgeWhenRendering: false,
  renderViewportOnly: false,
  motionBlurEnabled: true,
  motionSensitivityLevel: 1,
};

export default {
  namespaced: true,
  state,
};
