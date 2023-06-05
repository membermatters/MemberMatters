<template>
  <q-page class="column flex content-center justify-start">
    <q-banner
      v-if="!features.enableMembershipPayments"
      class="bg-warning text-dark q-mb-md"
    >
      {{ $t("tiers.disabledFeature") }}
    </q-banner>
    <br />
    <tiers-list />
  </q-page>
</template>

<script lang="ts">
import TiersList from "@components/AdminTools/TiersList.vue";
import { mapGetters } from "vuex";

export default {
  name: "ManageTiers",
  components: { TiersList },
  computed: {
    ...mapGetters("config", ["features"]),
  },
};
</script>
