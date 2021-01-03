<template>
  <div class="q-gutter-sm">
    <div class="text-h5">{{ $tc("tiers.selectToContinue") }}</div>
    <tier-card v-for="tier in tiers" :key="tier.id" :tier="tier" />
  </div>
</template>

<script>
import TierCard from "@components/Billing/TierCard.vue";

export default {
  name: "SelectTier",
  data() {
    return {
      tiers: [],
    };
  },
  components: {
    TierCard,
  },
  mounted() {
    this.getTiers();
  },
  methods: {
    getTiers() {
      this.$axios.get("/api/billing/tiers/").then((response) => {
        this.tiers = response.data;
      });
    },
  },
};
</script>
