<template>
  <div class="q-pa-md">
    <q-card class="shadow-5" :class="{ 'dark-border': $q.dark.isActive }">
      <div class="my-card column">
        <q-card-section>
          <div class="text-h6">{{ plan.name }}</div>
          <div class="text-subtitle2">
            {{
              $t("paymentPlans.intervalDescription", {
                currency: plan.currency.toUpperCase(),
                amount: $n(plan.cost / 100, "currency"),
                intervalCount: plan.intervalAmount,
                interval: $tc(
                  `paymentPlans.${
                    plan.intervalAmount > 1 ? "intervalPlurals" : "interval"
                  }.${plan.interval}`
                ),
              })
            }}
          </div>
        </q-card-section>

        <q-space />

        <template v-if="!selected">
          <q-separator />

          <q-card-section>
            <div class="row justify-center">
              <q-btn
                @click="selectPlan"
                color="primary"
                :label="$tc('button.select')"
              />
            </div>
          </q-card-section>
        </template>
      </div>
    </q-card>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  name: "PlanCard",
  props: {
    plan: {
      type: Object,
      required: true,
    },
    selected: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    selectPlan() {
      this.$emit("selected", this.plan);
    },
  },
});
</script>

<style lang="scss" scoped>
.my-card {
  height: 100%;
}

.q-card {
  height: 100%;
}

.dark-border {
  border: 1px solid;
}
</style>