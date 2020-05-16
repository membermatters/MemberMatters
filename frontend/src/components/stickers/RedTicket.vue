<template>
  <q-card
    id="sticker-image"
    class="bg-white text-dark"
  >
    <q-card-section
      style="height: 100%;"
      class="row flex no-wrap items-center justify-start q-pa-none"
    >
      <div class="column q-pl-xl q-py-lg">
        <p class="text-h3">
          <b>Finder:</b> {{ profile.fullName }}
        </p>

        <p class="text-h3 two-lines">
          <b>Description: </b> Lorem ipsum dolor sit amet, consectetur
          adipiscing elit, sed do eiusmod
          tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
          nostrud
          exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat
        </p>

        <p class="text-h3">
          <b>Date:</b> 02/02/20 <b>Exp:</b> 02/02/20
        </p>
      </div>

      <q-space />

      <q-img
        class="qrcode column"
        :src="qrcode"
      />
    </q-card-section>
  </q-card>
</template>

<script>
import { mapGetters } from 'vuex';
import QRCode from 'qrcode';
// import htmlToImage from 'html-to-image';
import icons from '../../icons';

export default {
  name: 'RedTicket',
  data() {
    return {
      qrcode: '',
    };
  },
  mounted() {
    this.getIdToken();
  },
  methods: {
    getIdToken() {
      QRCode.toDataURL('1,12345', { errorCorrectionLevel: 'H' }, async (err, url) => {
        this.qrcode = url;
      });
    },
  },
  computed: {
    ...mapGetters('config', ['siteOwner']),
    ...mapGetters('profile', ['profile']),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass" scoped>
  #sticker-image
    width: 991px
    max-width: 991px
    height: 306px

  .qrcode
    min-width: 306px

  p
    max-width: 100%
    text-overflow: ellipsis
    white-space: nowrap
    overflow: hidden
    margin-bottom: 8px
    font-size: 2.7rem

  .two-lines
    font-size: 2.3rem
    white-space: initial
    -webkit-line-clamp: 2
    display: -webkit-box
    -webkit-box-orient: vertical

</style>
