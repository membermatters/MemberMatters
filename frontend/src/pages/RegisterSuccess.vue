<template>
  <q-card class="fixed-center text-center q-pa-lg" style="max-width: 500px">
    <q-img
      v-if="images.siteLogo"
      fit="contain"
      :src="images.siteLogo"
      style="max-height: 40px; cursor: pointer"
      class="q-mt-md"
    />

    <q-icon v-else :name="icons.success" size="xl" color="success" />

    <br />
    <br />

    <p class="text-body1 text-faded">
      {{ $t("registrationCard.registrationComplete") }}
    </p>
    <q-btn
      color="primary-btn"
      style="width: 200px"
      to="/"
      :label="$t('button.continue')"
    />
  </q-card>
</template>

<script lang="ts">
import icons from "@icons";
import { mapGetters } from "vuex";

export default {
  name: "RegistrationSuccess",
  computed: {
    icons() {
      return icons;
    },
    ...mapGetters("config", ["images"]),
  },
};
</script>
