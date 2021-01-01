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
          <b>Extended Green Ticket</b>
        </h2>

        <p class="text-h3">
          <b>Approved By:</b> {{ approvedBy }}
        </p>

        <p class="text-h3">
          <b>Date Approved:</b> {{ dateApproved }}
        </p>

        <p class="text-h3">
          <b>Date Expires:</b> {{ dateExpires }}
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
import { mapGetters } from "vuex";
import QRCode from "qrcode";
import Moment from "moment";
import icons from "../../icons";

export default {
  name: "ExtendedGreenTicket",
  props: {
    approvedBy: {
      type: String,
      default: "No Name",
    },
    date: {
      type: String,
      default: "",
    },
    qrCodeId: {
      type: String,
      default: "0",
    },
  },
  data() {
    return {
      qrcode: "",
    };
  },
  mounted() {
    this.getQrCode();
  },
  methods: {
    getQrCode() {
      QRCode.toDataURL(`4,${this.qrCodeId}`, { errorCorrectionLevel: "H" }, async (err, url) => {
        this.qrcode = url;
      });
    },
  },
  computed: {
    ...mapGetters("config", ["siteOwner"]),
    ...mapGetters("profile", ["profile"]),
    icons() {
      return icons;
    },
    dateApproved() {
      return this.date.length ? Moment(this.date).format("DD/MM/YY") : Moment().format("DD/MM/YY");
    },
    dateExpires() {
      return this.date.length ? Moment(this.date).add(1, "month").format("DD/MM/YY") : Moment().add(1, "month").format("DD/MM/YY");
    },
  },
};
</script>

<style lang="sass" scoped>
@import "src/css/sticker"
</style>
