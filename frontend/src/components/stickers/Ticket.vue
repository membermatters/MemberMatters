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
          <b>{{ ticketType }}:</b> {{ profile.fullName }}
        </p>

        <p class="text-h3 two-lines">
          <b>{{ ticketDescription }}: </b> {{ description }}
        </p>

        <p class="text-h3">
          <b>Date:</b> {{ date }} <template v-if="!this.orange">
            <b>Exp:</b> {{ exp }}
          </template>
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
  name: "RedTicket",
  props: {
    red: {
      type: Boolean,
      default: false,
    },
    orange: {
      type: Boolean,
      default: false,
    },
    description: {
      type: String,
      default: "No Description",
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
    this.getIdToken();
  },
  methods: {
    getIdToken() {
      QRCode.toDataURL(`3,${this.qrCodeId}`, { errorCorrectionLevel: "H" }, async (err, url) => {
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
    date() {
      return Moment().format("DD/MM/YY"); // May 17th 2020, 1:30:47 pm
    },
    exp() {
      return Moment().add(14, "days").format("DD/MM/YY");
    },
    ticketType() {
      return this.red || this.orange ? "Finder" : "Owner";
    },
    ticketDescription() {
      return this.orange ? "Name" : "Description";
    },
  },
};
</script>

<style lang="sass" scoped>
@import "src/css/sticker"
</style>
