<template>
  <div class="q-gutter-md">
    <q-stepper v-model="step" ref="stepper" color="primary" animated>
      <q-step
        :name="1"
        :title="$tc('signup.induction')"
        :icon="icons.induction"
        :active-icon="icons.induction"
        :done="step > 1"
      >
        <div class="text-h6 q-py-md">
          {{ $tc("signup.completeInduction") }}
        </div>
        <div class="row items-stretch">
          <div style="width: 100%">
            <p>
              {{ $t("signup.completeInductionDescription") }}
            </p>

            <p>
              <b>
                {{ $t("signup.emailWarning", { email: profile.email }) }}
              </b>
            </p>
          </div>

          <template v-if="!inductionComplete">
            <div>
              <p>
                <a :href="features.inductionLink" target="_blank">
                  <img
                    class="q-pa-sm rounded-borders"
                    style="max-height: 70px; border: 1px solid"
                    src="@assets/img/canvas.png"
                  />
                </a>
              </p>
              <p>
                {{ $t("signup.waitingCompletion") }} <br />
                {{ $t("progress", { percent: inductionScore }) }}
              </p>
              <q-spinner size="2em"></q-spinner>
            </div>
          </template>

          <template v-else>
            <div class="q-pt-md">
              <p>
                {{ $t("signup.completedInduction") }}
              </p>
              <q-icon color="success" size="2em" :name="icons.success" />
            </div>
          </template>
        </div>

        <div class="row justify-start q-mt-md">
          <q-space />
          <q-btn
            @click="step++"
            :disable="!inductionComplete"
            color="primary"
            :label="$tc('button.continue')"
          />
        </div>
      </q-step>

      <q-step
        :name="2"
        :title="$tc('signup.accessCard')"
        :icon="icons.accessCard"
        :active-icon="icons.accessCard"
        :done="step > 2"
      >
        <div class="text-h6 q-py-md">
          {{ $tc("signup.assignAccessCard") }}
        </div>
        <div class="row items-stretch">
          <div style="width: 100%">
            <p>
              {{ $t("signup.assignAccessCardDescription") }}
            </p>

            <p>
              <b>
                {{
                  $t("signup.assignAccessCardWarning", { email: profile.email })
                }}
              </b>
            </p>

            <div>
              <q-input
                style="max-width: 300px"
                outlined
                v-model="accessCard"
                :label="$t('signup.accessCardNumber')"
              />
            </div>
          </div>
        </div>

        <div class="row justify-start q-mt-md">
          <q-space />
          <q-btn
            :disable="accessCardLoading"
            @click="submitAccessCard"
            color="primary"
            :label="$tc('button.continue')"
          />
        </div>
      </q-step>

      <q-step
        :name="3"
        :title="$tc('confirm')"
        :icon="icons.success"
        :active-icon="icons.success"
        :done="step > 2"
      >
        <template v-if="signupError">
          <div class="text-h6 q-py-md">
            {{ $tc("signup.error") }}
          </div>

          <div style="width: 100%">
            <p>
              {{ $t("signup.errorDescription", { email: contact.admin }) }}
            </p>

            <p>
              {{ $t("signup.errorMessageDescription") }}
              <br />
              <b>{{ signupErrorMessage }}</b>
              <br />
              <b>{{ signupErrorItems }}</b>
            </p>
          </div>
        </template>

        <template v-else>
          <div class="text-h6 q-py-md">
            {{ $tc("signup.submitted") }}
          </div>

          <div class="row items-stretch">
            <div style="width: 100%">
              <p>
                {{ $t("signup.submittedDescription") }}
              </p>
            </div>

            <div class="q-pt-md">
              <q-icon color="success" size="2em" :name="icons.success" />
            </div>
          </div>

          <div class="row justify-start q-mt-md">
            <q-space />
            <q-btn
              @click="$router.push({ name: 'dashboard' })"
              color="primary"
              :label="$tc('signup.continueToDashboard')"
            />
          </div>
        </template>
      </q-step>
    </q-stepper>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";
import { mapGetters } from "vuex";
import icons from "@icons";

export default defineComponent({
  name: "SignupRequiredSteps",
  props: {
    steps: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      step: 1,
      inductionComplete: false,
      accessCardComplete: false,
      accessCard: null,
      accessCardError: false,
      accessCardLoading: false,
      signupError: false,
      signupErrorMessage: "Unknown",
      signupErrorItems: [],
      inductionScore: 0,
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      interval: null as any,
    };
  },
  computed: {
    ...mapGetters("config", ["features", "contact"]),
    ...mapGetters("profile", ["profile"]),
    icons() {
      return icons;
    },
    allStepsDone() {
      if (this.steps.includes("induction")) {
        if (!this.inductionComplete) return false;
      }
      if (this.steps.includes("accessCard")) {
        if (!this.accessCardComplete) return false;
      }

      return true;
    },
  },
  mounted() {
    this.updateInductionStatus();
    this.interval = setInterval(async () => {
      this.updateInductionStatus();
    }, 10000);
  },
  beforeRouteLeave() {
    clearInterval(this.interval);
  },
  methods: {
    selectPlan() {
      this.$emit("selected", this.plan);
    },
    async updateInductionStatus() {
      let result = await this.$axios.post("/api/billing/check-induction/");
      this.inductionComplete = result.data.success;
      this.inductionScore = Math.floor(result.data.score);
      if (this.inductionComplete) {
        clearInterval(this.interval);
      }
    },
    async submitAccessCard() {
      this.accessCardLoading = true;
      await this.$axios
        .post("/api/billing/access-card/", {
          accessCard: this.accessCard,
        })
        .then((result) => {
          if (result.data.success) {
            this.$axios
              .post("/api/billing/complete-signup/")
              .then((result) => {
                if (!result.data.success) {
                  this.signupError = true;
                  this.signupErrorMessage = result.data.message;
                  this.signupErrorItems = result.data.items;
                } else {
                  this.signupError = false;
                }
              })
              .catch(() => {
                this.signupError = true;
              })
              .finally(() => {
                this.step++;
              });
          } else {
            this.accessCardError = true;
          }
        })
        .catch(() => {
          this.accessCardLoading = false;
          this.$q.dialog({
            title: this.$tc("error.error"),
            message: this.$tc("error.contactUs"),
          });
        });
    },
  },
});
</script>
