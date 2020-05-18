<template>
  <div class="q-pa-md">
    <q-card class="column flex items-center justify-center">
      <q-card-section>
        <h5 class="q-ma-none q-pa-sm">
          <q-icon
            class="rotate-90"
            :name="icons.rfid"
          /> {{ $t('loginRfidCard.swipeCard') }}
        </h5>

        <q-banner
          v-if="loginComplete"
          class="bg-positive text-white q-ma-md"
        >
          {{ $t('loginCard.loginSuccess') }}
        </q-banner>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import icons from 'src/icons';
import { mapGetters } from 'vuex';

export default {
  name: 'LoginRfidCard',
  data() {
    return {
      loginComplete: false,
    };
  },
  computed: {
    ...mapGetters('rfid', ['cardId']),
    icons() {
      return icons;
    },
  },
  watch: {
    cardId(card) {
      console.log(`got this ${card}`);
      this.loginComplete = true;
    },
  },
};
</script>
