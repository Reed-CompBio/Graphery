import { ActionTree, GetterTree, MutationTree } from 'vuex';
import { ContentRequestType, EditState, RootState } from '@/store/states/state';

const state: EditState = {
  content: {
    tutorialContent: {},
    graphInfoContent: {},
  },
};

const mutations: MutationTree<EditState> = {
  UPDATE_TUTORIAL_CONTENT(state, value: ContentRequestType) {
    state.content.tutorialContent[value.contentId] = value.content;
  },
  UPDATE_GRAPH_INFO_CONTENT(state, value: ContentRequestType) {
    state.content.tutorialContent[value.contentId] = value.content;
  },
};

const actions: ActionTree<EditState, RootState> = {};

const getters: GetterTree<EditState, RootState> = {
  tutorialContent(state) {
    return state.content.tutorialContent;
  },
  graphInfoContent(state) {
    return state.content.graphInfoContent;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
