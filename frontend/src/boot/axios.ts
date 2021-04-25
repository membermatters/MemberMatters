import axios, {AxiosStatic} from "axios";
import { Platform } from "quasar";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default ({ Vue, store }: {Vue: any, store: any}) => {
  const instance = axios.create({
    baseURL: process.env.apiBaseUrl || "",
    // withCredentials: true,
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFTOKEN",
  });

  // This interceptor adds the JWT to the request if it exists (ie mobile app)
  instance.interceptors.request.use(function (config) {
    const token = store.state.auth?.accessToken;

    if (Platform.is.capacitor && token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  });

  instance.interceptors.response.use(function (response) {
    return response;
  }, function (error) {
    if (error.response.status === 401) {
      store.commit("auth/setAuth", {});
      return Promise.reject(error);
    } else {
      return Promise.reject(error);
    }
  });

  Vue.prototype.$axios = instance;
};

declare module "vue/types/vue" {
  interface Vue {
    $axios: AxiosStatic;
  }
}
