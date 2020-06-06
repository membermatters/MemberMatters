<template>
  <div class="row">
    <div
      class="q-pa-md col-12 col-sm-4"
      v-for="action in quickActions"
      :key="action.title"
    >
      <a
        @click="action.click"
      >
        <q-card
          class="q-pa-xl column justify-center items-center"
        >
          <p class="text-h4">
            {{ action.title }}
          </p>
          <q-icon
            style="font-size: 100px"
            :name="action.icon"
          />
        </q-card>
      </a>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import icons from '@icons';

export default {
  name: 'QuickActions',
  methods: {
    doSignIn() {
      console.log('sign in triggered');

      this.$axios.post('/api/sitesessions/signin/', { guests: [] })
        .then(() => {
          this.$q.dialog({
            title: 'Success',
            message: this.$t('dashboard.signinSuccess'),
          });
        })
        .catch(() => {
          this.$q.dialog({
            title: 'Alert',
            message: this.$t('dashboard.signinError'),
          });
        });
    },
    doSignOut() {
      console.log('sign out triggered');

      this.$axios.put('/api/sitesessions/signout/')
        .then(() => {
          this.$router.push({ name: 'logout' });
        })
        .catch(() => {
          this.$q.dialog({
            title: 'Alert',
            message: this.$t('dashboard.signoutError'),
          });
        });
    },
  },
  computed: {
    ...mapGetters('profile', ['siteSignedIn']),
    quickActions() {
      const actions = [];

      if (this.siteSignedIn) {
        actions.push({
          title: 'Site Sign Out',
          icon: icons.logout,
          click: this.doSignOut,
        });
      } else {
        actions.push({
          title: 'Site Sign In',
          icon: icons.login,
          click: this.doSignIn,
        });
      }

      return actions;
    },
  },
};
</script>

<style scoped>
  a {
    text-decoration: none;
  }
  </style>
