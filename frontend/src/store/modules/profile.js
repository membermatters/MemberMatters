import axios from 'axios';

export default {
  namespaced: true,
  state: {
    loggedIn: false,
    memberStatus: 'Unknown',
    doorAccess: [],
    interlockAccess: [],
  },
  getters: {
    loggedIn: (state) => state.loggedIn,
    memberStatus: (state) => state.memberStatus,
    doorAccess: (state) => state.doorAccess,
    interlockAccess: (state) => state.interlockAccess,
  },
  mutations: {
    setLoggedIn(state, payload) {
      state.loggedIn = payload;
    },
    setMemberStatus(state, payload) {
      state.memberStatus = payload;
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
            commit('setMemberStatus', response.data.memberStatus);
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
