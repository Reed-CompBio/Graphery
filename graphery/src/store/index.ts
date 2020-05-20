import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import meta from '@/store/modules/meta';

export default new Vuex.Store({
  modules: {
    meta,
  },
  state: {},
  mutations: {},
  actions: {},
});
