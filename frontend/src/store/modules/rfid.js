export default {
  namespaced: true,
  state: {
    connected: false,
    readerUrl: 'ws://cardreader.local:81',
    cardId: null,
  },
  getters: {
    connected: (state) => state.connected,
    readerUrl: (state) => state.readerUrl,
    cardId: (state) => state.cardId,
  },
  mutations: {
    setConnected(state, payload) {
      state.connected = payload;
    },
    setReaderUrl(state, payload) {
      state.readerUrl = payload;
    },
    setCardId(state, payload) {
      state.cardId = payload;
    },
  },
};
