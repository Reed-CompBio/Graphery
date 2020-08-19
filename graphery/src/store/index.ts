import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import notifications from '@/store/modules/notifications';
import tutorials from '@/store/modules/tutorials';
import settings from '@/store/modules/settings';
import workspaces from '@/store/modules/workspaces';
import edits from '@/store/modules/edits';
import rj from '@/store/modules/ResultJsonStorage/ResultJsonStore';
import createPersistedState from 'vuex-persistedstate';
import { BaseState, UserType } from '@/store/states/state';

export default new Vuex.Store({
  // TODO Make it lazy load
  modules: {
    notifications,
    tutorials,
    settings,
    workspaces,
    edits,
    rj,
  },
  plugins: [createPersistedState({ paths: ['settings'] })],
  state: {
    drawer: false,
    csrfToken: null,
    user: null,
  } as BaseState,
  mutations: {
    CHANGE_DRAWER_STATE(state, value) {
      state.drawer = value;
    },
    SET_CSRF_TOKEN(state, token: string) {
      state.csrfToken = token;
    },
    SET_USER(state, userObj: UserType) {
      state.user = userObj;
    },
  },
  actions: {
    changeDrawerState({ commit }, value) {
      commit('CHANGE_DRAWER_STATE', value);
    },
    setUser({ commit }, user) {
      commit('SET_USER', user);
    },
  },
  getters: {
    noUser(state) {
      return state.user === null;
    },
  },
});
