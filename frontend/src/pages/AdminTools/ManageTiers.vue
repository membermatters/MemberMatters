<template>
  <q-page class="column flex content-center justify-start">
    <tiers-list />
  </q-page>
</template>

<script lang="ts">
import TiersList from "@components/AdminTools/TiersList.vue";

export default {
  name: "ManageTiers",
  components: { TiersList },
};
</script>
