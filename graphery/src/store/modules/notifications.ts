import { ActionTree, MutationTree, GetterTree } from 'vuex';
import { RootState, NotificationState } from '@/store/states/state';

const state: NotificationState = {
  info: false,
  warning: false,
  error: false,
  message: '',
  details: '',
};

const mutations: MutationTree<NotificationState> = {
  PUT_NOTIFICATION: (
    state,
    value: { type: string; messasge: string; details: string }
  ) => {
    state.message = value.messasge;
    state.details = value.details;
    if (value.type == 'i') {
      state.info = true;
    } else if (value.type == 'w') {
      state.warning = true;
    } else if (value.type == 'e') {
      state.error = true;
    }
  },
  CLEAR_NORIFICATION: (state) => {
    state.info = false;
    state.warning = false;
    state.error = false;
    state.message = '';
    state.details = '';
  },
};

const actions: ActionTree<NotificationState, RootState> = {
  putNotification(
    { commit },
    value: { type: string; messasge: string; details: string }
  ) {
    commit('PUT_NOTIFICATION', value);
  },
  clearNotification({ commit }) {
    commit('CLEAR_NORIFICATION');
  },
};

const getters: GetterTree<NotificationState, RootState> = {
  show(state) {
    return state.info || state.warning || state.error;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
