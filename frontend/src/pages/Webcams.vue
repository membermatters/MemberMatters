<template>
  <q-page class="row flex content-start justify-center q-mt-md">
    <div class="row flex flex-center">
      <p class="col-12 text-center q-px-md q-pt-md">
        {{ $t('webcams.pageDescription') }}
      </p>
      <div
        v-for="link in webcamLinks"
        class="col-xs-12 col-sm-6 q-pa-sm"
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
    max-width: 100vw;
  }
</style>
