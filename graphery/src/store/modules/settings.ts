import { RootState, SettingInfos, SettingState } from '@/store/states/state';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

const state: SettingState = {
  settingVer: '1.0.0',
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
  enableEditing: false,
  tabNum: 4,
  softTab: false,
  fontSize: 14,
  codeWrap: false,
  variableListHorizontal: false,

  // display
  pageDisplayNum: 5,
  language: 'en-us',
  tooltips: true,
  graphAbstractPopupShow: true,
};

const mutations: MutationTree<SettingState> = {
  CHANGE_DARK(state, value: boolean) {
    state.dark = value;
  },
  CHANGE_GRAPH_DARK(state, value: boolean) {
    state.graphDark = value;
  },
  CHANGE_HIDE_EDGE_WHEN_RENDERING(state, value: boolean) {
    state.hideEdgeWhenRendering = value;
  },
  CHANGE_RENDER_VIEWPORT_ONLY(state, value: boolean) {
    state.renderViewportOnly = value;
  },
  CHANGE_MOTION_BLUR_ENABLED(state, value: boolean) {
    state.motionBlurEnabled = value;
  },
  CHANGE_MOTION_SENSITIVITY_LEVEL(state, value: number) {
    state.motionSensitivityLevel = value;
  },
  CHANGE_GRAPH_SPLIT_POS(state, value: number) {
    state.graphSplitPos = value;
  },
  CHANGE_ENABLE_EDITING(state, value: boolean) {
    state.enableEditing = value;
  },
  CHANGE_TAB_NUM(state, value: number) {
    state.tabNum = value;
  },
  CHANGE_SOFT_TAB(state, value: boolean) {
    state.softTab = value;
  },
  CHANGE_FONT_SIZE(state, value: number) {
    state.fontSize = value;
  },
  CHANGE_CODE_WRAP(state, value: boolean) {
    state.codeWrap = value;
  },
  CHANGE_VARIABLE_LIST_ORIENTATION(state, value: boolean) {
    state.variableListHorizontal = value;
  },
  CHANGE_PAGE_DISPLAY_NUM(state, value: number) {
    state.pageDisplayNum = value;
  },
  CHANGE_LANGUAGE(state, value: string) {
    state.language = value;
  },
  CHANGE_TOOLTIPS(state, value: boolean) {
    state.tooltips = value;
  },
  CHANGE_GRAPH_ABSTRACT_POPUP_SHOW(state, value: boolean) {
    state.graphAbstractPopupShow = value;
  },
};

const actions: ActionTree<SettingState, RootState> = {
  changeDark({ commit }, dark: boolean) {
    commit('CHANGE_DARK', dark);
  },
  changeGraphDark({ commit }, graphDark: boolean) {
    commit('CHANGE_GRAPH_DARK', graphDark);
  },
  changeHideEdgeWhenRendering({ commit }, value: boolean) {
    commit('CHANGE_HIDE_EDGE_WHEN_RENDERING', value);
  },
  changeRenderViewportOnly({ commit }, value: boolean) {
    commit('CHANGE_RENDER_VIEWPORT_ONLY', value);
  },
  changeMotionBlurEnabled({ commit }, value: boolean) {
    commit('CHANGE_MOTION_BLUR_ENABLED', value);
  },
  changeMotionSensitivityLevel({ commit }, value: number) {
    commit('CHANGE_MOTION_SENSITIVITY_LEVEL', value);
  },
  changeGraphSplitPos({ commit }, value: number) {
    commit('CHANGE_GRAPH_SPLIT_POS', value);
  },
  changeEnableEditing({ commit }, value: boolean) {
    commit('CHANGE_ENABLE_EDITING', value);
  },
  changeTabNum({ commit }, value: number) {
    commit('CHANGE_TAB_NUM', value);
  },
  changeSoftTab({ commit }, value: boolean) {
    commit('CHANGE_SOFT_TAB', value);
  },
  changeFontSize({ commit }, value: number) {
    commit('CHANGE_FONT_SIZE', value);
  },
  changeCodeWrap({ commit }, value: boolean) {
    commit('CHANGE_CODE_WRAP', value);
  },
  changeVariableListOrientation({ commit }, value: boolean) {
    commit('CHANGE_VARIABLE_LIST_ORIENTATION', value);
  },
  changePageDisplayNum({ commit }, value: number) {
    commit('CHANGE_PAGE_DISPLAY_NUM', value);
  },
  changeLanguage({ commit }, value: string) {
    commit('CHANGE_LANGUAGE', value);
  },
  changeTooltips({ commit }, value: boolean) {
    commit('CHANGE_TOOLTIPS', value);
  },
  changeGraphAbstractPopupShow({ commit }, value: boolean) {
    commit('CHANGE_GRAPH_ABSTRACT_POPUP_SHOW', value);
  },
};

const getters: GetterTree<SettingState, RootState> = {
  graphBackgroundColor(state) {
    return state.graphDark ? '#1D1D1D' : '#ffffff';
  },
  getEnableEditing(state) {
    return state.enableEditing;
  },
  getFontSizeCss(state) {
    return `${state.fontSize}px`;
  },
  graphAbstractPopupShow(state) {
    return state.graphAbstractPopupShow;
  },
  getSettings(state) {
    return {
      [state.settingVer]: {
        // color
        dark: state.dark,
        graphDark: state.graphDark,
        // graph render
        hideEdgeWhenRendering: state.hideEdgeWhenRendering,
        renderViewportOnly: state.renderViewportOnly,
        motionBlurEnabled: state.motionBlurEnabled,
        motionSensitivityLevel: state.motionSensitivityLevel,
        graphSplitPos: state.graphSplitPos,
        // editor settings
        tabNum: state.tabNum,
        softTab: state.softTab,
        fontSize: state.fontSize,
        codeWrap: state.codeWrap,
        // display
        pageDisplayNum: state.pageDisplayNum,
        language: state.language,
        tooltips: state.tooltips,
      },
    };
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
