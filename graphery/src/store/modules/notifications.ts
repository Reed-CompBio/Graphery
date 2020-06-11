import { ActionTree, GetterTree, MutationTree } from 'vuex';
import {
  NotificationState,
  NotificationStatus,
  RootState,
} from '@/store/states/state';

const state: NotificationState = {
  status: NotificationStatus.empty,
  message: '',
  details: '',
};

const mutations: MutationTree<NotificationState> = {
  PUT_NOTIFICATION: (
    state,
    value: { status: NotificationStatus; message: string; details: string }
  ) => {
    ({
      status: state.status,
      message: state.message,
      details: state.details,
    } = value);
  },
  CLEAR_NOTIFICATION: (state) => {
    state.status = NotificationStatus.empty;
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
    commit('CLEAR_NOTIFICATION');
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
