<template>
  <q-page class="column flex justify-start items-center">
    <select-tier />
  </q-page>
</template>

<script>
import SelectTier from "@components/Billing/SelectTier.vue";

export default {
  name: "MembershipTierPage",
  components: {
    SelectTier,
  },
};
</script>
