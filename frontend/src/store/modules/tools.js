import Vue from "vue";

export default {
  namespaced: true,
  state: {
    lastSeen: [],
    recentSwipes: [],
    memberList: [],
    groupList: [],
    upcomingMeetings: [],
    proxies: [],
    members: [],
    memberBucksTransactions: [],
    memberBucksBalance: "",
    statistics: {},
  },
  getters: {
    lastSeen: (state) => state.lastSeen,
    recentSwipes: (state) => state.recentSwipes,
    memberList: (state) => state.memberList,
    groupList: (state) => state.groupList,
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
    setGroupList(state, payload) {
      state.groupList = payload;
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
        Vue.prototype.$axios.get("/api/tools/lastseen/")
          .then((result) => {
            commit("setLastSeen", result.data);
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
        Vue.prototype.$axios.get("/api/tools/swipes/")
          .then((result) => {
            commit("setRecentSwipes", result.data);
            resolve();
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    getMemberGroups({ commit }) {
      return new Promise((resolve, reject) => {
        Vue.prototype.$axios.get("/api/tools/groups/")
          .then((result) => {
            commit("setGroupList", result.data.groups);
            commit("setMemberList", result.data.members);
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
        Vue.prototype.$axios.get("/api/tools/meetings/")
          .then((result) => {
            commit("setUpcomingMeetings", result.data);
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
        Vue.prototype.$axios.get("/api/proxies/")
          .then((result) => {
            commit("setProxies", result.data);
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
        Vue.prototype.$axios.get("/api/tools/members/")
          .then((result) => {
            commit("setMembers", result.data);
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
        Vue.prototype.$axios.get("/api/memberbucks/transactions/")
          .then((result) => {
            commit("setMemberBucksTransactions", result.data);
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
        Vue.prototype.$axios.get("/api/memberbucks/balance/")
          .then((result) => {
            commit("setMemberBucksBalance", result.data.balance);
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
        Vue.prototype.$axios.get("/api/statistics/")
          .then((result) => {
            commit("setStatistics", result.data);
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
