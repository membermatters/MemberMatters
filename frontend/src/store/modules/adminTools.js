import Vue from 'vue';
import { i18n } from '../../boot/i18n';

export default {
  namespaced: true,
  state: {
    meetings: [],
    meetingTypes: [],
    kiosks: [],
    doors: [],
    interlocks: [],
    tiers: [],
  },
  getters: {
    meetings: (state) => state.meetings,
    meetingTypes: (state) => state.meetingTypes,
    kiosks: (state) => state.kiosks,
    doors: (state) => state.doors,
    interlocks: (state) => state.interlocks,
    tiers: (state) => state.tiers,
  },
  mutations: {
    setMeetings(state, payload) {
      state.meetings = payload;
    },
    setMeetingTypes(state, payload) {
      state.meetingTypes = payload;
    },
    setKiosks(state, payload) {
      state.kiosks = payload;
    },
    setDoors(state, payload) {
      state.doors = payload;
    },
    setInterlocks(state, payload) {
      state.interlocks = payload;
    },
    setTiers(state, payload) {
      state.tiers = payload;
    },
  },
  actions: {
    getMeetings({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get('/api/meetings/')
          .then((result) => {
            commit('setMeetings', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getMeetingTypes({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get('/api/meetings/types/')
          .then((result) => {
            // eslint-disable-next-line no-return-assign
            const results = result.data.map((type) => ({
              label: `${type.label} ${i18n.t('meetingForm.meeting')}`,
              value: type.value,
            }));
            commit('setMeetingTypes', results);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getKiosks({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get('/api/kiosks/')
          .then((result) => {
            commit('setKiosks', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getDoors({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get('/api/admin/doors/')
          .then((result) => {
            commit('setDoors', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getInterlocks({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get('/api/admin/interlocks/')
          .then((result) => {
            commit('setInterlocks', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getTiers({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get('/api/admin/tiers/')
          .then((result) => {
            commit('setTiers', result.data);
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
