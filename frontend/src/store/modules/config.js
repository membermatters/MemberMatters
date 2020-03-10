export default {
  namespaced: true,
  state: {
    siteName: 'MemberMatters Portal',
    siteOwner: 'MemberMatters',
    entityType: 'Association',
    homepageCards: {},
  },
  getters: {
    siteName: (state) => state.siteName,
    homepageCards: (state) => state.homepageCards,
  },
  mutations: {
    setSiteName(state, payload) {
      state.siteName = payload;
    },
    setHomepageCards(state, payload) {
      state.homepageCards = payload;
    },
  },
};
