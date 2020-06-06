import axios from 'axios';

export default ({ Vue }) => {
  Vue.prototype.$axios = axios.create({
    baseURL: process.env.apiBaseUrl || '',
    // withCredentials: true,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
  });
};
