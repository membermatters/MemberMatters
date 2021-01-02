import "axios";
import { Platform } from "quasar";

export default {
  namespaced: true,
  state: {
    accessToken: "",
    refreshToken: "",
  },
  getters: {
    accessToken: (state) => state.accessToken,
    refreshToken: (state) => state.refreshToken,
  },
  mutations: {
    setAuth(state, payload) {
      state.accessToken = payload.access;
      state.refreshToken = payload.refresh;
    },
  },
};
