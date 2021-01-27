<template>
  <q-page class="column flex justify-start items-center">
    <template v-if="!currentPlan">
      <template v-if="canSignup == null">
        <q-spinner size="4em" />
      </template>

      <template v-else-if="canSignup"><select-tier /></template>
      <template v-else>
        <div class="text-subtitle2">
          {{ $t("signup.requiredSteps") }}
        </div>
        <signup-required-steps :steps="requiredSteps" />
      </template>
    </template>

    <template v-else>
      <selected-tier :plan="currentPlan" :tier="currentTier" />

      <div v-if="cancelSuccess" class="row q-mb-md">
        <q-banner class="bg-success text-white">
          <div class="text-h5">{{ $tc("success") }}</div>
          <p>{{ $tc("paymentPlans.cancelSuccessDescription") }}</p>
        </q-banner>
      </div>

      <div v-if="subscriptionStatus === 'cancelling'" class="row q-mb-md">
        <q-banner class="bg-error text-white">
          <div class="text-h5">{{ $tc("paymentPlans.cancelling") }}</div>
          <p>
            {{
              $t("paymentPlans.cancellingDescription", { date: cancelAtDate })
            }}
          </p>
        </q-banner>
      </div>

      <div
        v-if="currentPeriodEnd && subscriptionStatus !== 'cancelling'"
        class="q-mb-md"
      >
        <div class="text-h6 q-py-md">
          {{ $t("paymentPlans.subscriptionInfo") }}
        </div>
        <q-card>
          <q-list bordered separator>
            <q-item>
              <q-item-section>
                <q-item-label>{{ currentPeriodEnd }}</q-item-label>
                <q-item-label caption>{{
                  $tc("paymentPlans.renewalDate")
                }}</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
                <q-item-label>{{ signupDate }}</q-item-label>
                <q-item-label caption>{{
                  $tc("paymentPlans.signupDate")
                }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </div>

      <q-btn
        v-if="subscriptionStatus === 'active'"
        :disable="disableButton"
        :loading="loadingButton"
        @click="cancelPlan"
        color="error"
        :label="$tc('paymentPlans.cancelButton')"
      />
      <q-btn
        v-else
        :disable="disableButton"
        :loading="loadingButton"
        @click="resumePlan"
        color="success"
        :label="$tc('paymentPlans.resumeButton')"
      />
    </template>
  </q-page>
</template>

<script>
import { defineComponent } from "@vue/composition-api";
import { mapGetters, mapActions } from "vuex";
import SelectTier from "@components/Billing/SelectTier.vue";
import SelectedTier from "@components/Billing/SelectedTier.vue";
import SignupRequiredSteps from "@components/Billing/SignupRequiredSteps.vue";

export default defineComponent({
  name: "MembershipTierPage",
  components: {
    SelectTier,
    SelectedTier,
    SignupRequiredSteps,
  },
  data() {
    return {
      requiredSteps: [],
      canSignup: null,
      requiredSteps: [],
      disableButton: false,
      loadingButton: false,
      cancelSuccess: false,
      subscriptionInfo: {
        billingCycleAnchor: null,
        currentPeriodEnd: null,
        cancelAt: null,
        cancelAtPeriodEnd: null,
        startDate: null,
      },
    };
  },
  computed: {
    ...mapGetters("profile", ["profile"]),
    currentPlan() {
      return this.profile.financial.membershipPlan;
    },
    currentTier() {
      return this.profile.financial.membershipTier;
    },
    subscriptionStatus() {
      return this.profile.financial.subscriptionState;
    },
    currentPeriodEnd() {
      return new Date(
        this.subscriptionInfo?.currentPeriodEnd * 1000
      ).toLocaleString("en-au");
    },
    signupDate() {
      return new Date(this.subscriptionInfo?.startDate * 1000).toLocaleString(
        "en-au"
      );
    },
    cancelAtDate() {
      return new Date(this.subscriptionInfo?.cancelAt * 1000).toLocaleString(
        "en-au"
      );
    },
  },
  methods: {
    ...mapActions("profile", ["getProfile"]),
    getSubscriptionInfo() {
      this.$axios.get("api/billing/myplan/").then((result) => {
        if (result.data.success) {
          this.subscriptionInfo = result.data.subscription;
        }
      });
    },
    getCanSignup() {
      this.$axios
        .get("api/billing/can-signup/")
        .then((result) => {
          if (result.data.success) {
            this.canSignup = true;
          } else {
            this.canSignup = false;
            this.requiredSteps = result.data.requiredSteps;
          }
        })
        .catch(() => {
          this.$q
            .dialog({
              title: this.$t("error.requestFailed"),
              message: this.$t("error.contactUs"),
            })
            .onDismiss(() => this.$router.push({ name: "dashboard" }));
        });
    },
    cancelPlan() {
      this.$q
        .dialog({
          title: this.$t("confirmAction"),
          message: this.$t("paymentPlans.cancelConfirmDescription"),
          cancel: this.$t("button.back"),
          persistent: true,
        })
        .onOk(() => {
          this.disableButton = true;
          this.loadingButton = true;
          this.$axios
            .post("api/billing/myplan/cancel/")
            .then((result) => {
              if (result.data.success) {
                this.cancelSuccess = true;
                setTimeout(() => {
                  location.reload();
                }, 3000);
              } else {
                this.$q.dialog({
                  title: this.$t("paymentPlans.cancelFailed"),
                  message: this.$t("error.contactUs"),
                });
                this.disableButton = false;
              }
            })
            .catch(() => {
              this.$q.dialog({
                title: this.$t("paymentPlans.cancelFailed"),
                message: this.$t("error.contactUs"),
              });
              this.disableButton = false;
            })
            .finally(() => {
              this.loadingButton = false;
            });
        });
    },
    resumePlan() {
      this.disableButton = true;
      this.loadingButton = true;
      this.$axios
        .post("api/billing/myplan/resume/")
        .then((result) => {
          if (result.data.success) {
            location.reload();
          } else {
            this.$q.dialog({
              title: this.$t("paymentPlans.resumeFailed"),
              message: this.$t("error.contactUs"),
            });
            this.disableButton = false;
          }
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t("paymentPlans.resumeFailed"),
            message: this.$t("error.contactUs"),
          });
          this.disableButton = false;
        })
        .finally(() => {
          this.loadingButton = false;
        });
    },
  },
  mounted() {
    this.getProfile();
    this.getSubscriptionInfo();
    this.getCanSignup();
  },
});
</script>
