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
  },
  methods: {
    ...mapMutations('config', ['setSiteName', 'setHomepageCards']),
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

    this.getPortalConfig();
  },
  computed: {
    ...mapGetters('config', ['siteName']),
    ...mapGetters('profile', ['loggedIn']),
  },
};
</script>
