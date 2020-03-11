import axios from 'axios';

export default {
  namespaced: true,
  state: {
    loggedIn: false,
    doorAccess: [],
    interlockAccess: [],
  },
  getters: {
    loggedIn: (state) => state.loggedIn,
    doorAccess: (state) => state.doorAccess,
    interlockAccess: (state) => state.interlockAccess,
  },
  mutations: {
    setLoggedIn(state, payload) {
      state.loggedIn = payload;
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
      axios.get('/api/access/permissions/')
        .then((response) => {
          commit('setDoorAccess', response.data.doors);
          commit('setInterlockAccess', response.data.interlocks);
        })
        .catch((error) => {
          throw error;
        });
    },
  },
};
