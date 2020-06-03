import Vue from 'vue';
import axios from 'axios';

Vue.prototype.$axios = axios;


// This tells axios where to find the CSRF token
Vue.prototype.$axios.defaults.xsrfCookieName = 'csrftoken';
Vue.prototype.$axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

if ((Vue.prototype.$q.platform.is.capacitor || Vue.prototype.$q.platform.is.electron) && process.env.NODE_ENV !== 'development') {
  Vue.prototype.$axios.defaults.baseURL = process.env.apiBaseUrl;
  console.log('env');
  console.log(process.env.apiBaseUrl);
}
