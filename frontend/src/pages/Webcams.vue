<template>
  <q-page class="q-mt-md">
    <div class="row flex flex-center">
      <p class="col-12 text-center q-pt-md">
        {{ $t('info.webcamPageDescription') }}
      </p>
      <div
        v-for="link in webcamLinks"
        class="col-6 q-pa-sm"
        :key="link[1]"
      >
        <q-img
          :src="`${link[1]}?interval=${interval}`"
        >
          <div class="absolute-bottom-right text-subtitle2">
            {{ link[0] }}
          </div>
        </q-img>
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'WebcamsPage',
  data() {
    return {
      interval: 0,
    };
  },
  mounted() {
    // This interval increments the query param every 60 seconds causing an image refresh
    setInterval(() => {
      this.interval++;
    }, 60000);
  },
  computed: {
    ...mapGetters('config', ['webcamLinks']),
  },
};
</script>

<style scoped>
  .row {
    width: 100%;
    max-width: 1200px;
  }
</style>
