<template>
  <q-page class="column flex justify-start items-center">
    <member-bucks-manage-billing style="width: 100%; max-width: 400px" />
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
