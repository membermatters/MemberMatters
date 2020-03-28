import axios from 'axios';

export default {
  namespaced: true,
  state: {
    meetings: [],
  },
  getters: {
    meetings: (state) => state.meetings,
  },
  mutations: {
    setMeetings(state, payload) {
      state.meetings = payload;
    },
  },
  actions: {
    getMeetings({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/meetings/')
          .then((result) => {
            commit('setMeetings', result.data);
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
