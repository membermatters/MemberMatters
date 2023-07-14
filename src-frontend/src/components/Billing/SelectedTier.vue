<template>
  <div class="q-pa-md">
    <div class="row">
      <div class="row col-xs-12 col-sm-6">
        <div class="text-h6 col-12">{{ $tc('tiers.selected') }}</div>
        <tier-card class="col-12" :tier="tier" selected />
      </div>
      <div class="row col-xs-12 col-sm-6">
        <div class="text-h6 col-12">{{ $tc('paymentPlans.selected') }}</div>
        <plan-card class="col-12" :plan="plan" selected />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import TierCard from '@components/Billing/TierCard.vue';
import PlanCard from '@components/Billing/PlanCard.vue';

export default defineComponent({
  name: 'SelectedTier',
  props: {
    plan: {
      type: Object,
      required: true,
    },
    tier: {
      type: Object,
      required: true,
    },
  },
  components: {
    TierCard,
    PlanCard,
  },
});
</script>
