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
        <h2 class="q-mt-none q-mb-md">
          <b>VISITOR TAG</b>
        </h2>

        <p class="text-h3">
          <b>Name:</b> {{ visitorName }}
        </p>

        <p class="text-h3">
          <b>Supervisor:</b> {{ supervisor }}
        </p>

        <p class="text-h3">
          <b>Issued:</b> {{ date }}
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
import Moment from 'moment';
import icons from '../../icons';

export default {
  name: 'ExtendedGreenTicket',
  props: {
    visitorName: {
      type: String,
      default: 'No Name',
    },
    supervisor: {
      type: String,
      default: 'None',
    },
    qrCodeId: {
      type: String,
      default: '0',
    },
  },
  data() {
    return {
      qrcode: '',
    };
  },
  mounted() {
    this.getQrCode();
  },
  methods: {
    getQrCode() {
      QRCode.toDataURL(`1,${this.qrCodeId}`, { errorCorrectionLevel: 'H' }, async (err, url) => {
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
    date() {
      return Moment().format('DD/MM/YY hh:mm a');
    },
  },
};
</script>

<style lang="sass" scoped>
@import "src/css/sticker"
</style>
