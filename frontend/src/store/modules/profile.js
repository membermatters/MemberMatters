export default {
  namespaced: true,
  state: {
    loggedIn: false,
  },
  getters: {
    loggedIn: (state) => state.loggedIn,
  },
  mutations: {
    setLoggedIn(state, payload) {
      state.loggedIn = payload;
    },
  },
};
