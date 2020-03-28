import Vuex from 'vuex';
import Vue from 'vue';
import VuexPersistence from 'vuex-persist';
import profile from './modules/profile';
import config from './modules/config';
import tools from './modules/tools';
import adminTools from './modules/adminTools';

Vue.use(Vuex);

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
});

export default new Vuex.Store({
  modules: {
    profile,
    config,
    tools,
    adminTools,
  },
  plugins: [vuexLocal.plugin],
});
