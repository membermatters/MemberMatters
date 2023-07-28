import address from 'address';
import sha256 from 'crypto-js/sha256';
import CryptoJS from 'crypto-js';
// import router from "../../router";
// import * as Sentry from "@sentry/vue";
// import { Integrations } from "@sentry/tracing";
// import { version } from "../../../package.json";
import { api } from 'boot/axios';

export default {
  namespaced: true,
  state: {
    siteName: 'MemberMatters Portal',
    siteOwner: 'MemberMatters',
    siteLocaleCurrency: 'en-AU',
    contact: {},
    homepageCards: {},
    webcamLinks: {},
    keys: {},
    features: {},
    kioskId: null,
    kioskIp: null,
    images: {},
    theme: {},
  },
  getters: {
    siteName: (state) => state.siteName,
    siteOwner: (state) => state.siteOwner,
    siteLocaleCurrency: (state) => state.siteLocaleCurrency,
    contact: (state) => state.contact,
    homepageCards: (state) => state.homepageCards,
    webcamLinks: (state) => state.webcamLinks,
    keys: (state) => state.keys,
    features: (state) => state.features,
    kioskId: (state) => state.kioskId,
    kioskIp: (state) => state.kioskIp,
    images: (state) => state.images,
    theme: (state) => state.theme,
  },
  mutations: {
    setSiteName(state, payload) {
      state.siteName = payload;
    },
    setSiteOwner(state, payload) {
      state.siteOwner = payload;
    },
    setSiteLocaleCurrency(state, payload) {
      state.siteLocaleCurrency = payload;
    },
    setContact(state, payload) {
      state.contact = payload;
    },
    setHomepageCards(state, payload) {
      state.homepageCards = payload;
    },
    setWebcamLinks(state, payload) {
      state.webcamLinks = payload;
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
    setImages(state, payload) {
      state.images = payload;
    },
    setTheme(state, payload) {
      state.theme = payload;
    },
  },
  actions: {
    getSiteConfig({ commit }) {
      return new Promise((resolve, reject) => {
        api
          .get('/api/config/')
          .then((result) => {
            commit('setSiteName', result.data.general.siteName);
            commit('setSiteOwner', result.data.general.siteOwner);
            commit(
              'setSiteLocaleCurrency',
              result.data.general.siteLocaleCurrency
            );
            commit('setContact', result.data.contact);
            commit('setHomepageCards', result.data.homepageCards);
            commit('setWebcamLinks', result.data.webcamLinks);
            commit('setKeys', result.data.keys);
            commit('setFeatures', result.data.features);
            commit('setImages', result.data.images);
            commit('setTheme', result.data.theme);

            // if (
            //   result.data.sentryDSN &&
            //   process.env.NODE_ENV !== "development"
            // ) {
            //   Sentry.init({
            //     Vue,
            //     dsn: result.data.sentryDSN,
            //     environment: process.env.NODE_ENV,
            //     release: version,
            //     integrations: [
            //       new Integrations.BrowserTracing({
            //         routingInstrumentation:
            //           Sentry.vueRouterInstrumentation(router),
            //         tracingOrigins: ["localhost", /^\//],
            //       }),
            //     ],
            //     initialScope: {
            //       tags: {
            //         siteOwner: result.data.general.siteOwner,
            //         siteContact: result.data.contact.sysadmin,
            //       },
            //     },
            //     // Set tracesSampleRate to 1.0 to capture 100%
            //     // of transactions for performance monitoring.
            //     // We recommend adjusting this value in production
            //     tracesSampleRate: 1.0,
            //   });
            // }

            const { analyticsId } = result.data;

            if (analyticsId) {
              ga('create', analyticsId, 'auto');
              ga('send', 'pageview');
            }

            resolve();
          })
          .catch((e) => {
            console.warn(e);
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
        api
          .put('/api/kiosks/', { name: state.kioskId, kioskId: state.kioskId })
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
