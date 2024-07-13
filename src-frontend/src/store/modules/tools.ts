// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import { api } from 'boot/axios';
import { MetricsApi, MetricsApiSchema } from 'types/api/metrics';

export default {
  namespaced: true,
  state: {
    lastSeen: [],
    recentSwipes: [],
    memberList: [],
    upcomingMeetings: [],
    proxies: [],
    members: [],
    memberBucksTransactions: [],
    memberBucksBalance: '',
    statistics: {} as MetricsApi,
  },
  getters: {
    lastSeen: (state) => state.lastSeen,
    recentSwipes: (state) => state.recentSwipes,
    memberList: (state) => state.memberList,
    upcomingMeetings: (state) => state.upcomingMeetings,
    proxies: (state) => state.proxies,
    members: (state) => state.members,
    memberBucksTransactions: (state) => state.memberBucksTransactions,
    memberBucksBalance: (state) => state.memberBucksBalance,
    statistics: (state) => state.statistics,
  },
  mutations: {
    setLastSeen(state, payload) {
      state.lastSeen = payload;
    },
    setRecentSwipes(state, payload) {
      state.recentSwipes = payload;
    },
    setMemberList(state, payload) {
      state.memberList = payload;
    },
    setUpcomingMeetings(state, payload) {
      state.upcomingMeetings = payload;
    },
    setProxies(state, payload) {
      state.proxies = payload;
    },
    setMembers(state, payload) {
      state.members = payload;
    },
    setMemberBucksTransactions(state, payload) {
      state.memberBucksTransactions = payload;
    },
    setMemberBucksBalance(state, payload) {
      state.memberBucksBalance = payload;
    },
    setStatistics(state, payload) {
      state.statistics = payload;
    },
  },
  actions: {
    getLastSeen({ commit }) {
      return new Promise((resolve, reject) => {
        api
          .get('/api/tools/lastseen/')
          .then((result) => {
            commit('setLastSeen', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getRecentSwipes({ commit }) {
      return new Promise((resolve, reject) => {
        api
          .get('/api/tools/swipes/')
          .then((result) => {
            commit('setRecentSwipes', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getUpcomingMeetings({ commit }) {
      return new Promise((resolve, reject) => {
        api
          .get('/api/tools/meetings/')
          .then((result) => {
            commit('setUpcomingMeetings', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getProxies({ commit }) {
      return new Promise((resolve, reject) => {
        api
          .get('/api/proxies/')
          .then((result) => {
            commit('setProxies', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getMembers({ commit }) {
      return new Promise((resolve, reject) => {
        api
          .get('/api/tools/members/')
          .then((result) => {
            commit('setMembers', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getMemberBucksTransactions({ commit }) {
      return new Promise((resolve, reject) => {
        api
          .get('/api/memberbucks/transactions/')
          .then((result) => {
            commit('setMemberBucksTransactions', result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getMemberBucksBalance({ commit }) {
      return new Promise((resolve, reject) => {
        api
          .get('/api/memberbucks/balance/')
          .then((result) => {
            commit('setMemberBucksBalance', result.data.balance);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getStatistics({ commit }) {
      return new Promise((resolve, reject) => {
        api.get('/api/statistics/').then((result) => {
          const data = MetricsApiSchema.safeParse(result.data); // Validate the response
          if (data.success) {
            commit('setStatistics', data.data);
            resolve();
          } else {
            reject(data.error);
          }
        });
      });
    },
  },
};
