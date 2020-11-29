import axios from 'axios';

export default ({ Vue, store }) => {
  const instance = axios.create({
    baseURL: process.env.apiBaseUrl || '',
    // withCredentials: true,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
  });

  // This interceptor adds the JWT to the request if it exists (ie mobile app)
  instance.interceptors.request.use(function (config) {
    const token = store.state.auth.accessToken;
    if (token) config.headers.Authorization = `Bearer ${token}`;

    return config;
  });

  Vue.prototype.$axios = instance;
};
