import axios from 'axios';

export default {
  namespaced: true,
  state: {
    siteName: 'MemberMatters Portal',
    siteOwner: 'MemberMatters',
    homepageCards: {},
    webcamLinks: {},
    groups: [],
    keys: {},
    features: {},
  },
  getters: {
    siteName: (state) => state.siteName,
    siteOwner: (state) => state.siteOwner,
    homepageCards: (state) => state.homepageCards,
    webcamLinks: (state) => state.webcamLinks,
    groups: (state) => state.groups,
    keys: (state) => state.keys,
    features: (state) => state.features,
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
    setGroups(state, payload) {
      state.groups = payload;
    },
    setKeys(state, payload) {
      state.keys = payload;
    },
    setFeatures(state, payload) {
      state.features = payload;
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
            commit('setKeys', result.data.keys);
            commit('setFeatures', result.data.features);
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
