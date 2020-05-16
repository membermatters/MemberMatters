import axios from 'axios';
import Moment from 'moment';
import idleTimeout from 'idle-timeout';
import { Platform } from 'quasar';

const getDefaultState = () => ({
  loggedIn: false,
  profile: {},
  doorAccess: [],
  interlockAccess: [],
});

export default {
  namespaced: true,
  state: getDefaultState(),
  getters: {
    loggedIn: (state) => state.loggedIn,
    profile: (state) => state.profile,
    doorAccess: (state) => state.doorAccess,
    interlockAccess: (state) => state.interlockAccess,
  },
  mutations: {
    resetState(state) {
      Object.assign(state, getDefaultState());
    },
    setLoggedIn(state, payload) {
      if (Platform.is.electron && payload === true) {
        window.IDLETIMEOUT = idleTimeout(
          () => {
            this.$router.push({ name: 'logout' });
          },
          {
            element: document,
            timeout: 1000 * 60,
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
  },
  actions: {
    getAccess({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/access/permissions/')
          .then((response) => {
            commit('setDoorAccess', response.data.doors);
            commit('setInterlockAccess', response.data.interlocks);
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
        axios.get('/api/profile/')
          .then((response) => {
            response.data.firstJoined = Moment(response.data.firstJoined).format('Do MMMM YYYY');
            commit('setProfile', response.data);
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
