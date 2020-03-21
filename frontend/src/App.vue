<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations, mapActions } from 'vuex';
import { colors } from 'quasar';
import store from './store/index';

colors.setBrand('dark', '#313131');


export default {
  name: 'App',
  store,
  watch: {
    $route() {
      this.updatePageTitle();
    },
    loggedIn(value) {
      if (!value) this.$router.push({ name: 'login' });
      if (value) this.getProfile();
    },
  },
  methods: {
    ...mapMutations('config', ['setSiteName', 'setHomepageCards', 'setWebcamLinks']),
    ...mapMutations('profile', ['setLoggedIn']),
    ...mapActions('config', ['getSiteConfig']),
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

  body.body--dark, .q-tab-panels--dark {
    background: #1f1f1f;
  }

  .q-table__bottom-nodata-icon {
    font-size: 200%;
    margin-right: 16px;
}
</style>
