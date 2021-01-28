<template>
  <div class="q-pa-md">
    <q-list bordered>
      <template v-if="steps.includes('induction')">
        <q-expansion-item
          group="somegroup"
          :icon="icons.induction"
          :label="$t('signup.completeInduction')"
          default-opened
          header-class="text-primary"
        >
          <q-card>
            <q-card-section>
              <p>
                {{ $t("signup.completeInductionDescription") }}
              </p>

              <a href="https://google.com" target="_blank">
                <img
                  class="q-pa-sm rounded-borders"
                  style="max-height: 70px; border: 1px solid"
                  src="@assets/img/canvas.png"
                />
              </a>

              <div class="q-pt-md">
                <p>
                  {{ $t("signup.waitingCompletion") }} <br />
                  Progress: {{ score }}%
                </p>
                <q-spinner size="2em"></q-spinner>
              </div>
            </q-card-section>
          </q-card>
        </q-expansion-item>

        <q-separator />
      </template>

      <template v-if="steps.includes('accessCard')">
        <q-expansion-item
          group="somegroup"
          :icon="icons.accessCard"
          :label="$t('signup.registerAccessCard')"
          header-class="text-teal"
        >
          <q-card>
            <q-card-section>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem,
              eius reprehenderit eos corrupti commodi magni quaerat ex numquam,
              dolorum officiis modi facere maiores architecto suscipit iste
              eveniet doloribus ullam aliquid.
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </template>
    </q-list>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";
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
      status: false,
      score: 0,
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      interval: null as any,
    };
  },
  computed: {
    icons() {
      return icons;
    },
  },
  mounted() {
    this.updateInductionStatus();
    this.interval = setInterval(async () => {
      this.updateInductionStatus();
    }, 5000);
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
      this.status = result.data.success;
      this.score = Math.floor(result.data.score);
    },
  },
});
</script>
