<template>
  <div id="q-app">
    <router-view />

    <q-dialog v-model="loginModal">
      <login-card
        no-redirect
        @loginComplete="loginModal = false"
      />
    </q-dialog>

    <settings v-if="$q.platform.is.electron" />
  </div>
</template>

<script>
// We should include Stripe everywhere to enable better fraud protection
import { loadStripe } from '@stripe/stripe-js';

import { mapActions, mapGetters, mapMutations } from 'vuex';
import Vue from 'vue';
import { colors, Dark, Platform } from 'quasar';
import Settings from 'components/Settings';
import store from './store/index';
import LoginCard from './components/LoginCard';


if (Platform.is.electron) {
  // eslint-disable-next-line global-require
  const { remote, webFrame } = require('electron');
  const { getCurrentWebContents, Menu, MenuItem } = remote;
  //
  let rightClickPosition;
  //
  const contextMenu = new Menu();
  const menuItem = new MenuItem(
    {
      label: 'Inspect Element',
      click: () => {
        const factor = webFrame.getZoomFactor();
        const x = Math.round(rightClickPosition.x * factor);
        const y = Math.round(rightClickPosition.y * factor);
        getCurrentWebContents().inspectElement(x, y);
      },
    },
  );
  contextMenu.append(menuItem);

  window.addEventListener(
    'contextmenu',
    (event) => {
      event.preventDefault();
      rightClickPosition = { x: event.x, y: event.y };
      contextMenu.popup();
    },
    false,
  );
}

colors.setBrand('dark', '#313131');

Vue.prototype.$stripeElementsStyle = () => ({
  style: {
    base: {
      color: Dark.isActive ? '#fff' : '#000',
      iconColor: Dark.isActive ? '#fff' : '#000',
      fontWeight: 400,
      fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
      fontSmoothing: 'antialiased',
      '::placeholder': {
        color: Dark.isActive ? '#fff' : '#000',
      },
    },
  },
});

export default {
  name: 'App',
  components: { Settings, LoginCard },
  store,
  data() {
    return {
      loginModal: false,
    };
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
  methods: {
    ...mapMutations('config', ['setSiteName', 'setHomepageCards', 'setWebcamLinks']),
    ...mapMutations('profile', ['setLoggedIn', 'resetState']),
    ...mapMutations('rfid', ['setConnected', 'setCardId']),
    ...mapActions('config', ['getSiteConfig', 'getKioskId', 'pushKioskId']),
    ...mapActions('profile', ['getProfile']),
    updatePageTitle() {
      const pageTitle = this.$route.meta.title;
      const nameKey = pageTitle ? `menuLink.${pageTitle}` : 'error.pageNotFound';
      document.title = `${this.$t(nameKey)} | ${this.siteName}`;
    },
    getPortalConfig() {
      this.getSiteConfig()
        .then(() => {
          this.updatePageTitle();
          if (this.features.stripe.enabled) {
            Vue.prototype.$stripe = loadStripe(this.keys.stripePublishableKey);
          }
        })
        .catch((error) => {
          throw error;
        });
    },
  },
  beforeCreate() {
    if (Platform.is.electron) {
      // eslint-disable-next-line global-require
      const { remote } = require('electron');

      this.$axios.interceptors.request.use(async (config) => {
        // Grab the csrf token
        const cookies = await remote.session.defaultSession.cookies.get(
          { url: process.env.apiBaseUrl },
        );

        if (!cookies.length) return config;

        const [csrfToken] = cookies.filter((cookie) => cookie.name === 'csrftoken');

        config.headers['X-CSRFTOKEN'] = csrfToken.value;

        return config;
      },
      (error) => {
        Promise.reject(error);
      });
    }

    this.$axios.interceptors.response.use((response) => response, (error) => {
    // Do something with response error
      if (error.response.status === 401 && !error.response.config.url.includes('/api/login/')) {
        this.setLoggedIn(false);
        this.resetState();
        this.$router.push('/login');
      }
      return Promise.reject(error);
    });
  },
  mounted() {
    if (Platform.is.electron) {
      this.getKioskId()
        .then(() => {
          this.pushKioskId();
        });
    }

    this.setCardId(null);

    // Get initial portal configuration data
    this.getPortalConfig();

    // Every 60 seconds check for new config data. This also checks that we're logged in.
    setInterval(() => {
      this.getPortalConfig();
    }, 60000);
  },
  computed: {
    ...mapGetters('config', ['siteName', 'keys', 'features']),
    ...mapGetters('profile', ['loggedIn']),
  },
};
</script>
