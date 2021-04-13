<template>
  <div class="q-gutter-md">
    <div class="text-h5 text-center">{{ $tc("tiers.becomeMember") }}</div>
    <q-stepper
      v-model="step"
      ref="stepper"
      color="primary"
      :done-icon="icons.success"
      :vertical="$q.screen.xs"
      animated
    >
      <q-step
        :name="1"
        :title="$tc('tiers.select')"
        :icon="icons.plans"
        :done="step > 1"
      >
        <div class="text-h6 q-py-md">
          {{ $tc("tiers.selectToContinue") }}
        </div>
        <div class="row items-stretch">
          <tier-card
            :class="{ featured: tier.featured }"
            class="col-xs-12 col-sm-6 col-md-4"
            style="min-width: 180px;"
            v-for="tier in tiers"
            :key="tier.id"
            :tier="tier"
            @selected="selectedTierEvent"
          />
        </div>
      </q-step>

      <q-step
        :name="2"
        :title="$tc('paymentPlans.select')"
        :icon="icons.dollar"
        :done="step > 2"
      >
        <div class="text-h6 q-py-md">
          {{ $tc("paymentPlans.selectToContinue") }}
        </div>

        <div class="row items-stretch">
          <plan-card
            class="col-xs-12 col-sm-6 col-md-4"
            v-for="plan in selectedTier.plans"
            :key="plan.id"
            :plan="plan"
            @selected="selectedPlanEvent"
          />
        </div>

        <div class="row justify-start">
          <q-btn
            class="q-mt-md"
            @click="backToTiers"
            flat
            :label="$tc('button.back')"
          />
        </div>
      </q-step>

      <q-step
        :name="3"
        :title="$tc('menuLink.billing')"
        :icon="icons.billing"
        :done="step > 3"
      >
        <div class="text-h6 q-py-md">
          {{ $tc("memberbucks.selectToContinue") }}
        </div>

        <member-bucks-manage-billing flat />

        <div class="row justify-start q-mt-md">
          <q-btn @click="backToPlans" flat :label="$tc('button.back')" />
          <q-space />
          <q-btn
            @click="selectedBillingMethodEvent"
            color="primary"
            :label="$tc('button.continue')"
          />
        </div>
      </q-step>

      <q-step
        :name="4"
        :title="$tc('paymentPlans.confirmSelection')"
        :icon="icons.success"
        :done="step > 4"
      >
        <div class="row">
          <div class="row col-xs-12 col-sm-6">
            <div class="text-h6 col-12">{{ $tc("tiers.selected") }}</div>
            <tier-card class="col-12" :tier="selectedTier" selected />
          </div>
          <div class="row col-xs-12 col-sm-6">
            <div class="text-h6 col-12">{{ $tc("paymentPlans.selected") }}</div>
            <plan-card class="col-12" :plan="selectedPlan" selected />
          </div>
        </div>

        <div class="text-h6">
          {{
            $t("paymentPlans.dueToday", {
              amount: $n(selectedPlan.cost / 100, "currency"),
            })
          }}
        </div>

        <p v-if="step > 2" class="q-py-md">
          {{
            $t("tiers.confirm", {
              intervalDescription: $t("paymentPlans.intervalDescription", {
                currency: selectedPlan.currency.toUpperCase(),
                amount: $n(selectedPlan.cost / 100, "currency"),
                intervalCount: selectedPlan.intervalAmount,
                interval: $tc(
                  `paymentPlans.${
                    selectedPlan.intervalAmount > 1
                      ? "intervalPlurals"
                      : "interval"
                  }.${selectedPlan.interval}`
                ),
              }),
            })
          }}
        </p>

        <div class="text-subtitle2 q-pb-md">
          {{ $t("tiers.confirmDelay") }}
        </div>

        <div v-if="finishSuccess" class="row">
          <q-banner class="bg-success text-white">
            <div class="text-h5">{{ $tc("paymentPlans.signupSuccess") }}</div>
            <p>{{ $tc("paymentPlans.signupSuccessDescription") }}</p>
          </q-banner>
        </div>

        <div v-else class="row">
          <q-btn
            flat
            :disable="disableFinish || loading"
            @click="backToBilling"
            :label="$tc('button.back')"
          />
          <q-space />
          <q-btn
            :loading="loading"
            :disable="disableFinish"
            @click="finishSignup"
            color="primary"
            :label="$tc('tiers.finish')"
          />
        </div>
      </q-step>
    </q-stepper>
    <div class="text-center">
      <p @click="skipSignup" style="text-decoration: underline; cursor: pointer;">
        {{ $tc("tiers.skipSignup") }}
      </p>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import { defineComponent } from "@vue/composition-api";
import TierCard from "@components/Billing/TierCard.vue";
import PlanCard from "@components/Billing/PlanCard.vue";
import MemberBucksManageBilling from "@components/MemberBucksManageBilling.vue";
import icons from "@icons";

export default defineComponent({
  name: "SelectTier",
  data() {
    return {
      step: 1,
      tiers: [],
      selectedTier: {},
      selectedPlan: {},
      disableFinish: false,
      loading: false,
      finishSuccess: false,
    };
  },
  computed: {
    icons() {
      return icons;
    },
  },
  components: {
    TierCard,
    PlanCard,
    MemberBucksManageBilling,
  },
  mounted() {
    this.getTiers();
  },
  methods: {
    ...mapActions("profile", ["getProfile"]),
    getTiers() {
      this.$axios.get("/api/billing/tiers/").then((response) => {
        this.tiers = response.data;
      });
    },
    skipSignup() {
      this.$axios
        .post("/api/billing/skip-signup/")
        .then(async (response) => {
          if (response.data.success) {
            await this.getProfile();
            this.$router.push({ name: "dashboard" });
          } else {
            this.$q.dialog({
              title: this.$t("error.requestFailed"),
              message: this.$t("error.contactUs"),
            });
          }
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t("error.requestFailed"),
            message: this.$t("error.contactUs"),
          });
        });
    },
    finishSignup() {
      this.disableFinish = true;
      this.loading = true;
      this.$axios
        .post(`api/billing/plans/${this.selectedPlan.id}/signup/`)
        .then((response) => {
          if (response.data.success) {
            this.finishSuccess = true;
            setTimeout(() => {
              location.reload();
            }, 3000);
          } else {
            this.disableFinish = false;
            this.$q.dialog({
              title: this.$t("paymentPlans.signupFailed"),
              message: this.$t("error.contactUs"),
            });
          }
        })
        .catch(() => {
          this.disableFinish = false;
          this.$q.dialog({
            title: this.$t("paymentPlans.signupFailed"),
            message: this.$t("error.contactUs"),
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    selectedTierEvent(tier) {
      this.selectedTier = tier;
      this.step++;
    },
    selectedPlanEvent(plan) {
      this.selectedPlan = plan;
      this.step++;
    },
    selectedBillingMethodEvent() {
      this.step++;
    },
    backToTiers() {
      this.step = 1;
      this.selectedPlan = {};
      this.selectedTier = {};
    },
    backToPlans() {
      this.step = 2;
      this.selectedPlan = {};
    },
    backToBilling() {
      this.step = 3;
    },
  },
});
</script>

<style lang="scss" scoped>
.featured {
  transform: scale(1.1);
}

.q-stepper__step-inner {
  width: 90vw;
  max-width: 1000px;
}
</style>
