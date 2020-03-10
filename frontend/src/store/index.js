import Vuex from 'vuex';
import Vue from 'vue';
import profile from './modules/profile';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    profile,
  },
});
