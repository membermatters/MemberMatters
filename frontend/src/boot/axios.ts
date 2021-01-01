import axios, { AxiosStatic } from "axios";

export default ({ Vue }: { Vue: any }, {store}: { store: any }) => {
  const instance = axios.create({
    baseURL: process.env.apiBaseUrl || "",
    // withCredentials: true,
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFTOKEN",
  });

  // This interceptor adds the JWT to the request if it exists (ie mobile app)
  instance.interceptors.request.use(function (config) {
    const token = store.state.auth.accessToken;
    if (token) config.headers.Authorization = `Bearer ${token}`;

    return config;
  });

  Vue.prototype.$axios = instance;
};

declare module "vue/types/vue" {
  interface Vue {
    $axios: AxiosStatic;
  }
}