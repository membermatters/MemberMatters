<template>
  <div id="q-app">
    <router-view />

    <q-dialog v-model="loginModal">
      <login-card no-redirect @login-complete="loginModal = false" />
    </q-dialog>

    <settings v-if="$q.platform.is.electron" />
  </div>
</template>

<script>
// We should include Stripe everywhere to enable better fraud protection
import { loadStripe } from "@stripe/stripe-js";
import { mapActions, mapGetters, mapMutations } from "vuex";
import Vue from "vue";
import { colors, Dark, Platform } from "quasar";
import Settings from "components/Settings";
import store from "./store/index";
import LoginCard from "./components/LoginCard";
import { Plugins } from "@capacitor/core";
const { SplashScreen } = Plugins;

colors.setBrand("dark", "#313131");

Vue.prototype.$stripeElementsStyle = () => ({
  style: {
    base: {
      color: Dark.isActive ? "#fff" : "#000",
      iconColor: Dark.isActive ? "#fff" : "#000",
      fontWeight: 400,
      fontFamily: "Roboto, Open Sans, Segoe UI, sans-serif",
      fontSmoothing: "antialiased",
      "::placeholder": {
        color: Dark.isActive ? "#fff" : "#000",
      },
    },
  },
});

export default {
  name: "App",
  components: { Settings, LoginCard },
  store,
  data() {
    return {
      loginModal: false,
    };
  },
  computed: {
    ...mapGetters("config", ["siteName", "keys", "features", "theme"]),
    ...mapGetters("profile", ["loggedIn"]),
  },
  watch: {
    $route() {
      this.updatePageTitle();
    },
    loggedIn(value) {
      // if (!value) this.$router.push({ name: 'login' });
      if (value) this.getProfile();
    },
  },
  beforeCreate() {
    if (Platform.is.electron) {
      this.$axios.interceptors.request.use(
        async (config) => {
          // Grab the csrf token
          var cookie = this.$q.cookies.get("cookie_name");

          if (!cookie) return config;

          config.headers["X-CSRFTOKEN"] = cookie;

          return config;
        },
        (error) => {
          Promise.reject(error);
        }
      );
    }

    this.$axios.interceptors.response.use(
      (response) => response,
      (error) => {
        // Do something with response error
        console.log(error);
        if (
          error.response.status === 401 &&
          !error.response.config.url.includes("/api/login/")
        ) {
          this.setLoggedIn(false);
          this.resetState();
          if (!window.location.pathname.includes("/profile/password/reset")) {
            this.$router.push("/login");
          }
        }
        return Promise.reject(error);
      }
    );
  },
  mounted() {
    if (Platform.is.electron) {
      this.getKioskId().then(() => {
        this.pushKioskId();
      });
    }

    this.setCardId(null);

    // Get initial portal configuration data
    this.getPortalConfig();
  },
  methods: {
    ...mapMutations("config", [
      "setSiteName",
      "setHomepageCards",
      "setWebcamLinks",
    ]),
    ...mapMutations("profile", ["setLoggedIn", "resetState"]),
    ...mapMutations("rfid", ["setConnected", "setCardId"]),
    ...mapActions("config", ["getSiteConfig", "getKioskId", "pushKioskId"]),
    ...mapActions("profile", ["getProfile"]),
    updatePageTitle() {
      const pageTitle = this.$route.meta.title;
      const nameKey = pageTitle
        ? `menuLink.${pageTitle}`
        : "error.pageNotFound";
      document.title = `${this.$t(nameKey)} | ${this.siteName}`;
    },
    getPortalConfig() {
      this.getSiteConfig()
        .then(() => {
          this.updatePageTitle();
          if (this.features.stripe.enabled) {
            try {
              Vue.prototype.$stripe = loadStripe(this.keys.stripePublishableKey);
            } catch {
              console.log("Failed to load Stripe...");
            }
          }
            colors.setBrand("primary", this.theme?.themePrimary || "#278ab0");
            colors.setBrand("secondary", this.theme?.themeToolbar || "#0461b1");
            colors.setBrand("accent", this.theme?.themeAccent || "#189ab4");
        })
        .catch((e) => {
          console.error(e);
          console.error("Unable to get portal config!");
        });
    },
  },
};
</script>
