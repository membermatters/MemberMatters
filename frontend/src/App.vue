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
    ...mapGetters("auth", ["refreshToken"]),
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
    this.$axios.interceptors.response.use(
      (response) => response,
      (error) => {
        // If we get a 401 and it's not the loggedin check endpoint, or reset password/login page, redirect user to login screen
        if (
          error.response &&
          error.response.status === 401 &&
          !error.response.config.url.includes("/api/loggedin/")
        ) {
          // this means our access token probably just expired so request a new one
          if (
            error.response.data.code === "token_not_valid" &&
            Platform.is.capacitor &&
            error.response.data?.messages[0]?.token_class === "AccessToken"
          ) {
            this.$axios
              .post("/api/token/refresh/", {
                refresh: this.refreshToken,
              })
              .then((response) => {
                this.setAuth(response.data);
                this.setLoggedIn(true);
                return Promise.resolve();
              })
              .catch(() => {
                // if we fail to refresh, send them back to the login page
                this.$router.push("/login");
                return Promise.resolve();
              });
          } else {
            this.setLoggedIn(false);
            this.resetState();
            if (
              !window.location.pathname.includes("/profile/password/reset") &&
              !window.location.pathname.includes("/login")
            ) {
              this.$router.push("/login");
              return Promise.resolve();
            }
          }
        }
        return Promise.reject(error);
      }
    );
  },
  async mounted() {
    if (Platform.is.electron) {
      this.getKioskId().then(() => {
        this.pushKioskId();
      });
    }

    this.setCardId(null);

    // Get initial portal configuration data
    await this.getPortalConfig();
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
    ...mapMutations("auth", ["setAuth"]),
    updatePageTitle() {
      const pageTitle = this.$route.meta.title;
      const nameKey = pageTitle
        ? `menuLink.${pageTitle}`
        : "error.pageNotFound";
      document.title = `${this.$t(nameKey)} | ${this.siteName}`;
    },
    getPortalConfig() {
      return new Promise((resolve, reject) => {
        this.getSiteConfig()
          .then(() => {
            this.updatePageTitle();
            if (this.features.enableStripe) {
              try {
                Vue.prototype.$stripe = loadStripe(
                  this.keys.stripePublishableKey
                );
              } catch {
                console.log("Failed to load Stripe...");
              }
            }
            colors.setBrand("primary", this.theme?.themePrimary || "#278ab0");
            colors.setBrand("secondary", this.theme?.themeToolbar || "#0461b1");
            colors.setBrand("accent", this.theme?.themeAccent || "#189ab4");
            resolve();
          })
          .catch((e) => {
            console.error(e);
            console.error("Unable to get portal config!");
            reject(e);
          });
      });
    },
  },
};
</script>
