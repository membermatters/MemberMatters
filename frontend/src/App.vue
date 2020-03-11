<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations } from 'vuex';
import store from './store/index';


export default {
  name: 'App',
  store,
  data() {
    return {
      portalConfig: {
        general: { siteName: 'MemberMatters Portal', siteOwner: 'MemberMatters' },
        images: { siteLogo: '/media/logo.png', siteFavicon: '/media/favicon.png' },
        homepageCards: {},
      },
    };
  },
  watch: {
    $route() {
      this.updatePageTitle();
    },
    loggedIn(value) {
      if (!value) this.$router.push({ name: 'login' });
    },
  },
  methods: {
    ...mapMutations('config', ['setSiteName', 'setHomepageCards', 'setWebcamLinks']),
    ...mapMutations('profile', ['setLoggedIn']),
    updatePageTitle() {
      const pageTitle = this.$route.meta.title;
      const nameKey = pageTitle ? `menuLink.${pageTitle}` : 'error.pageNotFound';
      document.title = `${this.$t(nameKey)} | ${this.siteName}`;
    },
    getPortalConfig() {
      axios.get('/api/config')
        .then((result) => {
          this.portalConfig = result.data;
          this.setSiteName(this.portalConfig.general.siteName);
          this.setHomepageCards(this.portalConfig.homepageCards);
          this.setLoggedIn(this.portalConfig.loggedIn);
          this.setWebcamLinks(this.portalConfig.webcamLinks);
          this.updatePageTitle();
        })
        .catch((error) => {
          throw error;
        });
    },
  },
  mounted() {
    // This tells axios where to find the CSRF token
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

    // This sets the default axios base URL to the django dev server if we're on the dev server
    // eslint-disable-next-line no-restricted-globals
    if (location.port === '8080') {
      // eslint-disable-next-line no-restricted-globals
      axios.defaults.baseURL = `http://${location.hostname}:8000`;
    }

    // Get initial portal configuration data
    this.getPortalConfig();

    // Every 60 seconds check for new config data. This also checks that we're logged in.
    setInterval(() => {
      this.getPortalConfig();
    }, 60000);
  },
  computed: {
    ...mapGetters('config', ['siteName']),
    ...mapGetters('profile', ['loggedIn']),
  },
};
</script>

<style>
  .q-page {
    max-width: 1000px;
    margin: auto;
  }
</style>
