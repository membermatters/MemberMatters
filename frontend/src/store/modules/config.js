import axios from 'axios';

export default {
  namespaced: true,
  state: {
    siteName: 'MemberMatters Portal',
    siteOwner: 'MemberMatters',
    mainMenuOpen: false,
    homepageCards: {},
    webcamLinks: {},
    groups: [],
  },
  getters: {
    siteName: (state) => state.siteName,
    siteOwner: (state) => state.siteOwner,
    homepageCards: (state) => state.homepageCards,
    webcamLinks: (state) => state.webcamLinks,
    groups: (state) => state.groups,
  },
  mutations: {
    setSiteName(state, payload) {
      state.siteName = payload;
    },
    setSiteOwner(state, payload) {
      state.siteOwner = payload;
    },
    setMainMenuOpen(state, payload) {
      state.mainMenuOpen = payload;
    },
    setHomepageCards(state, payload) {
      state.homepageCards = payload;
    },
    setWebcamLinks(state, payload) {
      state.webcamLinks = payload;
    },
    setGroups(state, payload) {
      state.groups = payload;
    },
  },
  actions: {
    getSiteConfig({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/config/')
          .then((result) => {
            commit('setSiteName', result.data.general.siteName);
            commit('setSiteOwner', result.data.general.siteOwner);
            commit('setHomepageCards', result.data.homepageCards);
            commit('setWebcamLinks', result.data.webcamLinks);
            commit('setGroups', result.data.groups);
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
