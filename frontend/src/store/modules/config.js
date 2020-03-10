export default {
  namespaced: true,
  state: {
    siteName: 'MemberMatters Portal',
    homepageCards: {},
    webcamLinks: {},
  },
  getters: {
    siteName: (state) => state.siteName,
    homepageCards: (state) => state.homepageCards,
    webcamLinks: (state) => state.webcamLinks,
  },
  mutations: {
    setSiteName(state, payload) {
      state.siteName = payload;
    },
    setHomepageCards(state, payload) {
      state.homepageCards = payload;
    },
    setWebcamLinks(state, payload) {
      state.webcamLinks = payload;
    },
  },
};
