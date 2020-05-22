import { ActionTree, MutationTree, GetterTree } from 'vuex';
import { RootState, NotificationState } from '@/store/states/state';

const state: NotificationState = {
  status: '',
  message: '',
  details: '',
};

const mutations: MutationTree<NotificationState> = {
  PUT_NOTIFICATION: (
    state,
    value: { status: string; message: string; details: string }
  ) => {
    ({
      status: state.status,
      message: state.message,
      details: state.details,
    } = value);
  },
  CLEAR_NORIFICATION: (state) => {
    state.status = '';
    state.message = '';
    state.details = '';
  },
};

const actions: ActionTree<NotificationState, RootState> = {
  putNotification(
    { commit },
    value: { status: string; message: string; details: string }
  ) {
    // TODO what about multiple notifications?
    commit('PUT_NOTIFICATION', value);
  },
  clearNotification({ commit }) {
    commit('CLEAR_NORIFICATION');
  },
};

const getters: GetterTree<NotificationState, RootState> = {
  show(state) {
    return state.status != '';
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
