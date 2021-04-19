import "axios";
import { Plugins } from "@capacitor/core";
const { Storage } = Plugins;

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
  actions: {
    async retrieveAuth ({ commit }) {
      const accessToken = await Storage.get({ key: "accessToken" });
      const refreshToken = await Storage.get({ key: "refreshToken"});
      commit("setAuth", {access: accessToken.value, refresh: refreshToken.value});
    },
  },
  mutations: {
    async setAuth(state, payload) {
      state.accessToken = payload.access;
      state.refreshToken = payload.refresh;
      await Storage.set({
        key: "accessToken",
        value: payload.access
      });
      await Storage.set({
        key: "refreshToken",
        value: payload.refresh
      });
    },
  },
};
