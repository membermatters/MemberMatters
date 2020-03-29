import axios from 'axios';
import { i18n } from '../../boot/i18n';

export default {
  namespaced: true,
  state: {
    meetings: [],
    meetingTypes: [],
  },
  getters: {
    meetings: (state) => state.meetings,
    meetingTypes: (state) => state.meetingTypes,
  },
  mutations: {
    setMeetings(state, payload) {
      state.meetings = payload;
    },
    setMeetingTypes(state, payload) {
      state.meetingTypes = payload;
    },
  },
  actions: {
    getMeetings({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/meetings/')
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
        axios.get('/api/meetings/types/')
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
  },
};
