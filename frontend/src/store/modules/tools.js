import axios from 'axios';

export default {
  namespaced: true,
  state: {
    lastSeen: [],
    recentSwipes: [],
  },
  getters: {
    lastSeen: (state) => state.lastSeen,
    recentSwipes: (state) => state.recentSwipes,
  },
  mutations: {
    setLastSeen(state, payload) {
      state.lastSeen = payload;
    },
    setRecentSwipes(state, payload) {
      state.recentSwipes = payload;
    },
  },
  actions: {
    getLastSeen({ commit }) {
      axios.get('/api/tools/lastseen/')
        .then((result) => {
          commit('setLastSeen', result.data);
        })
        .catch((error) => {
          throw error;
        });
    },
  },
};
