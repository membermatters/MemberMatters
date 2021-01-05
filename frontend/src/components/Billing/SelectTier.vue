<template>
  <div class="q-gutter-md">
    <div class="text-h5 text-center">{{ $tc("tiers.becomeMember") }}</div>
    <q-stepper v-model="step" ref="stepper" color="primary" animated>
      <q-step
        :name="1"
        :title="$tc('tiers.select')"
        :icon="icons.plans"
        :done="step > 1"
      >
        <div class="row">
          <tier-card
            :class="{ featured: tier.featured }"
            class="col-xs-12 col-sm-6 col-md-4"
            v-for="tier in tiers"
            :key="tier.id"
            :tier="tier"
          />
        </div>
      </q-step>

      <q-step
        :name="2"
        :title="$tc('paymentPlans.select')"
        :icon="icons.dollar"
        :done="step > 2"
      >
        An ad group contains one or more ads which target a shared set of
        keywords.
      </q-step>
    </q-stepper>
  </div>
</template>

<script>
import TierCard from "@components/Billing/TierCard.vue";
import icons from "@icons";

export default {
  name: "SelectTier",
  data() {
    return {
      step: 1,
      tiers: [],
    };
  },
  computed: {
    icons() {
      return icons;
    },
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

<style lang="scss" scoped>
.featured {
  transform: scale(1.1);
}
</style>