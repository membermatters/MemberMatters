import axios from 'axios';

export default {
  namespaced: true,
  state: {
    lastSeen: [],
    recentSwipes: [],
    memberList: [],
    groupList: [],
    upcomingMeetings: [],
    members: [],
  },
  getters: {
    lastSeen: (state) => state.lastSeen,
    recentSwipes: (state) => state.recentSwipes,
    memberList: (state) => state.memberList,
    groupList: (state) => state.groupList,
    upcomingMeetings: (state) => state.upcomingMeetings,
    members: (state) => state.members,
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
    setMembers(state, payload) {
      state.members = payload;
    },
  },
  actions: {
    getLastSeen({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/tools/lastseen/')
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
        axios.get('/api/tools/swipes/')
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
    getMemberGroups({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/tools/groups/')
          .then((result) => {
            commit('setGroupList', result.data.groups);
            commit('setMemberList', result.data.members);
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
        axios.get('/api/tools/meetings/')
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
    getMembers({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/tools/members/')
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
  },
};
