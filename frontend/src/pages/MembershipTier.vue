<template>
  <q-page class="column flex justify-start items-center">
    <template v-if="!currentPlan">
      <select-tier />
    </template>

    <template v-else>
      <selected-tier :plan="currentPlan" :tier="currentTier" />
    </template>
  </q-page>
</template>

<script>
import { defineComponent } from "@vue/composition-api";
import { mapGetters, mapActions } from "vuex";
import SelectTier from "@components/Billing/SelectTier.vue";
import SelectedTier from "@components/Billing/SelectedTier.vue";

export default defineComponent({
  name: "MembershipTierPage",
  components: {
    SelectTier,
    SelectedTier,
  },
  computed: {
    ...mapGetters("profile", ["profile"]),
    currentPlan() {
      return this.profile.financial.membershipPlan;
    },
    currentTier() {
      return this.profile.financial.membershipTier;
    },
  },
  methods: {
    ...mapActions("profile", ["getProfile"]),
  },
  mounted() {
    this.getProfile();
  },
});
</script>
