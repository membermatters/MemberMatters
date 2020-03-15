import axios from 'axios';

export default {
  namespaced: true,
  state: {
    loggedIn: false,
    profile: {},
    doorAccess: [],
    interlockAccess: [],
  },
  getters: {
    loggedIn: (state) => state.loggedIn,
    profile: (state) => state.profile,
    doorAccess: (state) => state.doorAccess,
    interlockAccess: (state) => state.interlockAccess,
  },
  mutations: {
    setLoggedIn(state, payload) {
      state.loggedIn = payload;
    },
    setProfile(state, payload) {
      state.profile = payload;
    },
    setDoorAccess(state, payload) {
      state.doorAccess = payload;
    },
    setInterlockAccess(state, payload) {
      state.interlockAccess = payload;
    },
  },
  actions: {
    getAccess({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/access/permissions/')
          .then((response) => {
            commit('setDoorAccess', response.data.doors);
            commit('setInterlockAccess', response.data.interlocks);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getProfile({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/profile/')
          .then((response) => {
            commit('setProfile', response.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
  },
};
