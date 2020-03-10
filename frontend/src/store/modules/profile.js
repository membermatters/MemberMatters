export default {
  namespaced: true,
  state: {
    loggedIn: false,
  },
  getters: {
    loggedIn: (state) => state.loggedIn,
  },
  mutations: {
    loggedIn(state, payload) {
      state.usersTeams = payload;
    },
  },
};
