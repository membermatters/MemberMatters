<template>
  <q-page class="column flex justify-start items-center">
    <member-bucks-manage-billing />
  </q-page>
</template>

<script>
import MemberBucksManageBilling from "@components/MemberBucksManageBilling.vue";

export default {
  name: "ManageBillingPage",
  components: {
    MemberBucksManageBilling,
  },
};
</script>
