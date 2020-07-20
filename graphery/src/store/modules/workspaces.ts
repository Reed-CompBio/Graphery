import { ActionTree, GetterTree, MutationTree } from 'vuex';
import {
  CodeHistoryState,
  CodeInstance,
  RootState,
  WorkSpaceState,
} from '@/store/states/state';
import get = Reflect.get;

const state: WorkSpaceState = {
  tutorialSpace: {
    codes: [],
    currentIndex: -1,
  },
  playgroundSpace: {
    codes: [],
    currentIndex: -1,
  },
};

const mutations: MutationTree<WorkSpaceState> = {
  ADD_NEW_WORKSPACE_TO_TUTORIAL(state, value: CodeInstance) {
    state.tutorialSpace.codes.push(value);
  },
  ADD_NEW_WORKSPACE_TO_PLAYGROUND(state, value: CodeInstance) {
    state.playgroundSpace.codes.push(value);
  },
  ADD_HISTORY(
    state,
    value: {
      code: CodeInstance;
      codeHash: string;
      execHistory: CodeHistoryState;
    }
  ) {
    value.code.execHistories[value.codeHash] = value.execHistory;
  },
  CHANGE_TUTORIAL_WORKSPACE_INDEX(state, index: number) {
    if (state.tutorialSpace.codes.length === 0) {
      state.tutorialSpace.currentIndex = -1;
    } else {
      state.tutorialSpace.currentIndex = index;
    }
  },
  CHANGE_PLAYGROUND_WORKSPACE_INDEX(state, index: number) {
    if (state.tutorialSpace.codes.length === 0) {
      state.tutorialSpace.currentIndex = -1;
    } else {
      state.tutorialSpace.currentIndex = index;
    }
  },
};

const actions: ActionTree<WorkSpaceState, RootState> = {
  addNewWorkSpaceToTutorial({ commit }, codeString: string) {
    commit('ADD_NEW_WORKSPACE_TO_TUTORIAL', {
      code: codeString,
      lastModified: Date(),
      history: [codeString],
    });
  },
  addNewWorkSpaceToPlayground({ commit }, codeString: string) {
    commit('ADD_NEW_WORKSPACE_TO_PLAYGROUND', {
      code: codeString,
      lastModified: Date(),
      history: [codeString],
    });
  },
  addHistoryToCurrentTutorialWorkSpace(
    { commit, getters },
    value: { codeHash: string; codeHistory: CodeHistoryState }
  ) {
    commit('ADD_HISTORY', { code: getters.currentTutorialWorkSpace, ...value });
  },
  addHistoryToCurrentPlaygroundWorkSpace(
    { commit, getters },
    value: { codeHash: string; codeHistory: CodeHistoryState }
  ) {
    commit('ADD_HISTORY', {
      code: getters.currentPlaygroundWorkSpace,
      ...value,
    });
  },
  changeTutorialWorkSpaceIndex({ commit }, value: number) {
    commit('CHANGE_TUTORIAL_WORKSPACE_INDEX', value);
  },
  changePlaygroundWorkSpaceIndex({ commit }, value: number) {
    commit('CHANGE_PLAYGROUND_WORKSPACE_INDEX', value);
  },
};

const getters: GetterTree<WorkSpaceState, RootState> = {
  currentTutorialWorkSpace(state) {
    const index = state.tutorialSpace.currentIndex;
    if (index < 0) {
      return null;
    } else {
      return state.tutorialSpace.codes[index];
    }
  },
  currentTutorialCodeHistories(state, getters) {
    return (
      getters.currentTutorialWorkSpace &&
      getters.currentTutorialWorkSpace.history
    );
  },
  currentPlaygroundWorkSpace(state) {
    const index = state.playgroundSpace.currentIndex;
    if (index < 0) {
      return null;
    } else {
      return state.tutorialSpace.codes[index];
    }
  },
  currentPlaygroundCodeHistories(state, getters) {
    return;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
