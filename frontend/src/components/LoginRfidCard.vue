<template>
  <div class="q-pa-md">
    <q-card class="column flex items-center justify-center">
      <q-card-section>
        <h5 class="q-ma-none q-pa-sm row justify-center">
          <q-icon
            class="rotate-90 q-mt-xs q-mr-sm"
            style="font-size: 90%;"
            :name="connected ? icons.rfid : icons.rfidSlash"
          /> {{ $t('loginRfidCard.swipeCard') }}
        </h5>

        <br v-if="loginComplete || loginFailed || loginError">

        <q-banner
          v-if="loginComplete"
          class="bg-positive text-white q-ma-md"
        >
          {{ $t('loginCard.loginSuccess') }}
        </q-banner>

        <q-banner
          v-if="loginFailed"
          class="bg-negative text-white"
        >
          {{ $t('loginRfidCard.failed') }}
        </q-banner>

        <q-banner
          v-if="loginError"
          class="bg-negative text-white"
        >
          {{ $t('error.requestFailed') }}
        </q-banner>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import icons from 'src/icons';
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: 'LoginRfidCard',
  data() {
    return {
      loginComplete: false,
      loginFailed: false,
      loginError: false,
    };
  },
  methods: {
    ...mapMutations('profile', ['setLoggedIn']),
  },
  computed: {
    ...mapGetters('rfid', ['cardId', 'connected']),
    ...mapGetters('config', ['kioskId']),
    icons() {
      return icons;
    },
  },
  watch: {
    cardId(card) {
      this.$axios.post('/api/login/kiosk/', { cardId: card, kioskId: this.kioskId })
        .then(() => {
          this.loginComplete = true;
          this.loginFailed = false;
          this.loginError = false;
          this.$emit('login-complete');
          setTimeout(() => {
            this.setLoggedIn(true);
            this.$router.push({ name: 'dashboard' });
          }, 1000);
        })
        .catch((error) => {
          if (error.response.status === 401) this.loginFailed = true;
          else this.loginError = true;
        });
    },
  },
};
</script>
