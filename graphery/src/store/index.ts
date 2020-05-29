import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import notifications from '@/store/modules/notifications';
import tutorials from '@/store/modules/tutorials';
import settings from '@/store/modules/settings';
import createPersistedState from 'vuex-persistedstate';

export default new Vuex.Store({
  modules: {
    notifications,
    tutorials,
    settings,
  },
  plugins: [createPersistedState({ paths: ['settings'] })],
  state: {
    drawer: false,
  },
  mutations: {
    CHANGE_DRAWER_STATE(state, value) {
      state.drawer = value;
    },
  },
  actions: {
    changeDrawerState({ commit }, value) {
      commit('CHANGE_DRAWER_STATE', value);
    },
  },
});
