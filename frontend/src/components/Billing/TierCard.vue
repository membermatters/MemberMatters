<template>
  <div class="q-pa-md">
    <q-card class="shadow-5" :class="{ 'dark-border': $q.dark.isActive }">
      <div class="my-card column">
        <q-card-section>
          <div class="text-h6">{{ tier.name }}</div>
          <div v-if="!selected" class="text-subtitle2 q-pb-sm">
            {{
              $t("tiers.plansFrom", {
                plan: $t("paymentPlans.intervalDescription", {
                  currency: minPrice.currency.toUpperCase(),
                  amount: $n(minPrice.cost / 100, "currency"),
                  intervalCount: minPrice.intervalAmount,
                  interval: $tc(
                    `paymentPlans.${
                      minPrice.intervalAmount > 1
                        ? "intervalPlurals"
                        : "interval"
                    }.${minPrice.interval}`
                  ),
                }),
              })
            }}
          </div>
          <div class="text-subtitle2">{{ tier.description }}</div>
        </q-card-section>

        <q-space />

        <template v-if="!selected">
          <q-separator />

          <q-card-section>
            <div class="row justify-center">
              <q-btn
                @click="selectTier"
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
  name: "TierCard",
  props: {
    tier: {
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
    selectTier() {
      this.$emit("selected", this.tier);
    },
  },
  computed: {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    minPrice(): any {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      return this.tier.plans.reduce((prev: any, curr: any) => {
        return prev.cost < curr.cost ? prev : curr;
      });
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