import address from 'address';
import sha256 from 'crypto-js/sha256';
import CryptoJS from 'crypto-js';
import Vue from 'vue';

export default {
  namespaced: true,
  state: {
    siteName: 'MemberMatters Portal',
    siteOwner: 'MemberMatters',
    homepageCards: {},
    webcamLinks: {},
    groups: [],
    memberTypes: [],
    keys: {},
    features: {},
    kioskId: null,
    kioskIp: null,
  },
  getters: {
    siteName: (state) => state.siteName,
    siteOwner: (state) => state.siteOwner,
    homepageCards: (state) => state.homepageCards,
    webcamLinks: (state) => state.webcamLinks,
    groups: (state) => state.groups,
    memberTypes: (state) => state.memberTypes,
    keys: (state) => state.keys,
    features: (state) => state.features,
    kioskId: (state) => state.kioskId,
    kioskIp: (state) => state.kioskIp,
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
    setmemberTypes(state, payload) {
      state.memberTypes = payload;
    },
    setKeys(state, payload) {
      state.keys = payload;
    },
    setFeatures(state, payload) {
      state.features = payload;
    },
    setKioskId(state, payload) {
      state.kioskId = payload;
    },
    setKioskIp(state, payload) {
      state.kioskIp = payload;
    },
  },
  actions: {
    getSiteConfig({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get('/api/config/')
          .then((result) => {
            commit('setSiteName', result.data.general.siteName);
            commit('setSiteOwner', result.data.general.siteOwner);
            commit('setHomepageCards', result.data.homepageCards);
            commit('setWebcamLinks', result.data.webcamLinks);
            commit('setGroups', result.data.groups);
            commit('setmemberTypes', result.data.memberTypes);
            commit('setKeys', result.data.keys);
            commit('setFeatures', result.data.features);
            const { analyticsId } = result.data;

            if (analyticsId) {
              ga('create', analyticsId, 'auto');
              ga('send', 'pageview');
            }

            resolve();
          })
          .catch((error) => {
            reject();
          });
      });
    },
    getKioskId({ commit }) {
      return new Promise((resolve) => {
        commit('setKioskIp', address.ip());
        address.mac((err, macAddress) => {
          commit('setKioskId', sha256(macAddress).toString(CryptoJS.enc.Hex));
          resolve();
        });
      });
    },
    pushKioskId({ state }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.put('/api/kiosks/', { name: state.kioskId, kioskId: state.kioskId })
          .then((result) => {
            resolve(result);
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
  },
};
