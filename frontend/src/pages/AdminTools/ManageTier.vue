<template>
  <q-page class="column flex content-center justify-start">
    <plans-list />
  </q-page>
</template>

<script lang="ts">
import PlansList from "@components/AdminTools/TiersList.vue";

export default {
  name: "ManageTier",
  components: { PlansList },
};
</script>
