<template>
  <q-page class="flex flex-center">
    <q-spinner
      v-if="spinner"
      color="primary-btn"
      size="3em"
    />

    <q-banner
      v-if="!spinner"
      class="bg-positive text-white"
    >
      {{ $t('info.logoutSuccess') }}
    </q-banner>

    <q-banner
      v-if="error"
      class="bg-negative text-white"
    >
      {{ $t('error.logoutFailed') }}
    </q-banner>
  </q-page>
</template>

<script>
import axios from 'axios';
import { mapMutations } from 'vuex';

export default {
  name: 'LogoutPage',
  data() {
    return {
      error: false,
      spinner: true,
    };
  },
  mounted() {
    axios
      .post('/api/logout/')
      .then((response) => {
        if (response.data.success === true) {
          this.completeLogout();
        } else {
          this.error = true;
        }
      })
      .catch((error) => {
        if (error.response.status === 401) {
          this.completeLogout();
        } else {
          throw error;
        }
      });
  },
  methods: {
    ...mapMutations('profile', ['setLoggedIn', 'resetState']),
    completeLogout() {
      this.resetState();
      this.setLoggedIn(false);
      this.error = false;
      this.spinner = false;
      setTimeout(() => {
        this.$router.push({ name: 'login' });
      }, 2000);
    },
  },
};
</script>
