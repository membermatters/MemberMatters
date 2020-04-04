<template>
  <div id="q-app">
    <router-view />

    <q-dialog v-model="loginModal">
      <login-card
        no-redirect
        @loginComplete="loginModal = false"
      />
    </q-dialog>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex';
import { colors } from 'quasar';
import store from './store/index';
import LoginCard from './components/LoginCard';

colors.setBrand('dark', '#313131');

export default {
  name: 'App',
  components: { LoginCard },
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
  beforeCreate() {
    this.$axios.interceptors.response.use((response) => response, (error) => {
    // Do something with response error
      if (error.response.status === 401) {
        this.setLoggedIn(false);
        this.resetState();
        this.loginModal = true;
      }
      return Promise.reject(error);
    });
  },
  mounted() {
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
