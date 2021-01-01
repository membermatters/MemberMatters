<template>
  <q-page class="column flex content-center justify-start">
    <manage-tier />
  </q-page>
</template>

<script lang="ts">
import ManageTier from "@components/AdminTools/ManageTier.vue";

export default {
  name: "ManageTierPage",
  components: { ManageTier },
};
</script>
