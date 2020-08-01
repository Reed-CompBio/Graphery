import { ActionTree, GetterTree, MutationTree } from 'vuex';
import {
  CodeHistoryState,
  WorkSpaceInstance,
  RootState,
  WorkSpaceState,
} from '@/store/states/state';

const state: WorkSpaceState = {
  tutorialSpace: {
    workspaces: [],
  },
  playgroundSpace: {
    workspaces: [],
  },
};

const mutations: MutationTree<WorkSpaceState> = {
  ADD_NEW_WORKSPACE_TO_TUTORIAL(state, value: WorkSpaceInstance) {
    state.tutorialSpace.workspaces.push(value);
  },
  ADD_NEW_WORKSPACE_TO_PLAYGROUND(state, value: WorkSpaceInstance) {
    state.playgroundSpace.workspaces.push(value);
  },
  ADD_HISTORY(
    state,
    value: {
      currentWorkSpace: WorkSpaceInstance;
      codeHash: string;
      execHistory: CodeHistoryState;
    }
  ) {
    value.currentWorkSpace.execHistories[value.codeHash] = value.execHistory;
  },
};

const actions: ActionTree<WorkSpaceState, RootState> = {
  addNewWorkSpaceToTutorial(
    { commit },
    info: { name: string; codeString: string }
  ) {
    commit('ADD_NEW_WORKSPACE_TO_TUTORIAL', {
      name: info.name,
      code: info.codeString,
      lastModified: Date(),
      history: [info.codeString],
    });
  },
  addNewWorkSpaceToPlayground(
    { commit },
    info: { name: string; codeString: string }
  ) {
    commit('ADD_NEW_WORKSPACE_TO_PLAYGROUND', {
      name: info.name,
      code: info.codeString,
      lastModified: Date(),
      history: [info.codeString],
    });
  },
  addHistoryToCurrentTutorialWorkSpace(
    { commit, getters },
    value: {
      currentWorkSpace: WorkSpaceInstance;
      codeHash: string;
      codeHistory: CodeHistoryState;
    }
  ) {
    commit('ADD_HISTORY', value);
  },
  addHistoryToCurrentPlaygroundWorkSpace(
    { commit, getters },
    value: {
      currentWorkSpace: WorkSpaceInstance;
      codeHash: string;
      codeHistory: CodeHistoryState;
    }
  ) {
    commit('ADD_HISTORY', value);
  },
  changeTutorialWorkSpaceIndex({ commit }, value: number) {
    commit('CHANGE_TUTORIAL_WORKSPACE_INDEX', value);
  },
  changePlaygroundWorkSpaceIndex({ commit }, value: number) {
    commit('CHANGE_PLAYGROUND_WORKSPACE_INDEX', value);
  },
};

const getters: GetterTree<WorkSpaceState, RootState> = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
