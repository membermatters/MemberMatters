import Moment from "moment";
import idleTimeout from "idle-timeout";
import { Platform } from "quasar";
import Vue from "vue";

const getDefaultState = () => ({
  loggedIn: false,
  profile: {},
  doorAccess: [],
  interlockAccess: [],
  siteSignedIn: false,
});

export default {
  namespaced: true,
  state: getDefaultState(),
  getters: {
    loggedIn: (state) => state.loggedIn,
    profile: (state) => state.profile,
    doorAccess: (state) => state.doorAccess,
    interlockAccess: (state) => state.interlockAccess,
    siteSignedIn: (state) => state.siteSignedIn,
  },
  mutations: {
    resetState(state) {
      Object.assign(state, getDefaultState());
    },
    setLoggedIn(state, payload) {
      // If we're on electron, logged in, and not in dev then enable auto logout after 60s
      if (Platform.is.electron && payload === true && process.env.NODE_ENV !== "Development") {
        window.IDLETIMEOUT = idleTimeout(
          () => {
            this.$router.push({ name: "logout" });
          },
          {
            element: document,
            timeout: 1000 * 20,
            loop: false,
          },
        );
      }
      state.loggedIn = payload;
    },
    setProfile(state, payload) {
      state.profile = payload;
    },
    setDoorAccess(state, payload) {
      state.doorAccess = payload;
    },
    setInterlockAccess(state, payload) {
      state.interlockAccess = payload;
    },
    setSiteSignedIn(state, payload) {
      state.siteSignedIn = payload;
    },
  },
  actions: {
    getAccess({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get("/api/access/permissions/")
          .then((response) => {
            commit("setDoorAccess", response.data.doors);
            commit("setInterlockAccess", response.data.interlocks);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getProfile({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get("/api/profile/")
          .then((response) => {
            response.data.firstJoined = Moment(response.data.firstJoined).format("Do MMMM YYYY");
            commit("setProfile", response.data);
            commit("setLoggedIn", true);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getLoggedIn({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get("/api/loggedin/")
          .then(() => {
            commit("setLoggedIn", true);
            resolve();
          })
          .catch((error) => {
            commit("setLoggedIn", false);
            resolve();
          });
      });
    },
    getSiteSignedIn({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get("/api/sitesessions/check/")
          .then((response) => {
            commit("setSiteSignedIn", response.data);
            resolve();
          })
          .catch((error) => {
            resolve();
          });
      });
    },
  },
};
