<template>
  <q-card id="sticker-image" class="bg-white text-dark">
    <q-card-section
      style="height: 100%"
      class="row flex no-wrap items-center justify-start q-pa-none"
    >
      <div
        class="column q-px-lg q-py-lg"
        style="max-width: 100%; max-height: 100%"
      >
        <p class="text-h3 four-lines">
          {{ description }}
        </p>

        <p class="text-h3">
          <b>{{ safeToUse }}</b>
        </p>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { mapGetters } from 'vuex';
import icons from '../../icons';

export default {
  name: 'OrangeTicketDetails',
  props: {
    description: {
      type: String,
      default: 'No Further Details',
    },
    safe: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapGetters('config', ['siteOwner']),
    ...mapGetters('profile', ['profile']),
    icons() {
      return icons;
    },
    safeToUse() {
      return this.safe
        ? 'This MAY be safe to use, proceed with caution.'
        : 'This is NOT safe to use currently.';
    },
  },
};
</script>

<style lang="sass" scoped>
@import "src/css/sticker"
</style>
