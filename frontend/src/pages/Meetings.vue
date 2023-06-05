<template>
  <q-page class="column flex content-center justify-start">
    <q-banner
      v-if="!features.enableProxyVoting"
      class="bg-warning text-dark q-mb-md"
    >
      {{ $t("tiers.disabledFeature") }}
    </q-banner>

    <meetings-list />
  </q-page>
</template>

<script lang="ts">
import MeetingsList from "@components/MeetingsList.vue";
import { mapGetters } from "vuex";

export default {
  name: "MeetingsPage",
  components: { MeetingsList },
  computed: {
    ...mapGetters("config", ["features", "images"]),
  },
};
</script>
