import axios from 'axios';

export default {
  namespaced: true,
  state: {
    siteName: 'MemberMatters Portal',
    siteOwner: 'MemberMatters',
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
    setSiteOwner(state, payload) {
      state.siteOwner = payload;
    },
    setHomepageCards(state, payload) {
      state.homepageCards = payload;
    },
    setWebcamLinks(state, payload) {
      state.webcamLinks = payload;
    },
  },
  actions: {
    getSiteConfig({ commit }) {
      axios.get('/api/config/')
        .then((result) => {
          commit('setSiteName', result.data.general.siteName);
          commit('setSiteOwner', result.data.general.siteOwner);
          commit('setHomepageCards', result.data.homepageCards);
          // this.setLoggedIn(result.data.loggedIn);
          commit('setWebcamLinks', result.data.webcamLinks);
        })
        .catch((error) => {
          throw error;
        });
    },
  },
};
