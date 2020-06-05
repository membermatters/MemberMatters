<template>
  <div class="row">
    <div
      class="q-pa-md col-12 col-sm-4"
      v-for="action in quickActions"
      :key="action.title"
    >
      <router-link
        :to="action.to"
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
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import icons from '@icons';

export default {
  name: 'QuickActions',
  computed: {
    ...mapGetters('profile', ['siteSignedIn']),
    quickActions() {
      const actions = [];

      if (this.siteSignedIn) {
        actions.push({
          title: 'Site Sign Out',
          icon: icons.logout,
          to: { name: 'siteSignOut' },
        });
      } else {
        actions.push({
          title: 'Site Sign In',
          icon: icons.login,
          to: { name: 'siteSignIn' },
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
