import { TutorialState, RootState } from '@/store/states/state';
import { MutationTree, ActionTree, Action, GetterTree } from 'vuex';

const state: TutorialState = {
  article: '',
  graphs: null,
  codes: null,
};

const mutations: MutationTree<TutorialState> = {};

const actions: ActionTree<TutorialState, RootState> = {};

const getters: GetterTree<TutorialState, RootState> = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
