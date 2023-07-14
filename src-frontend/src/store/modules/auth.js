import 'axios';
import { Storage } from '@capacitor/storage';

export default {
  namespaced: true,
  state: {
    accessToken: '',
    refreshToken: '',
  },
  getters: {
    accessToken: (state) => state.accessToken,
    refreshToken: (state) => state.refreshToken,
  },
  actions: {
    async retrieveAuth({ commit }) {
      const accessToken = await Storage.get({ key: 'accessToken' });
      const refreshToken = await Storage.get({ key: 'refreshToken' });
      commit('setAuth', {
        access: accessToken.value,
        refresh: refreshToken.value,
      });
    },
  },
  mutations: {
    async setAuth(state, payload) {
      if (payload.access || payload.access === '') {
        state.accessToken = payload.access;
        await Storage.set({
          key: 'accessToken',
          value: payload.access,
        });
      }

      if (payload.refresh || payload.refresh === '') {
        state.refreshToken = payload.refresh;
        await Storage.set({
          key: 'refreshToken',
          value: payload.refresh,
        });
      }
    },
  },
};
