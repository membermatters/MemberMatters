<template>
  <q-page class="row flex content-start justify-center q-mt-md">
    <div class="row flex flex-center">
      <p class="text-body1 col-12 text-center q-px-md q-pt-md">
        {{ $t('webcams.pageDescription') }}
      </p>

      <div
        v-for="link in webcamLinks"
        :key="link[1]"
        class="col-xs-12 col-sm-6 q-pa-sm"
      >
        <q-img :src="`${link[1]}?timestamp=${timestamp}`">
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
      timestamp: new Date().getTime(),
    };
  },
  mounted() {
    // This changes the query param every 60 seconds causing an image refresh
    setInterval(() => {
      this.timestamp = new Date().getTime();
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
