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
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem,
              eius reprehenderit eos corrupti commodi magni quaerat ex numquam,
              dolorum officiis modi facere maiores architecto suscipit iste
              eveniet doloribus ullam aliquid.
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
  computed: {
    icons() {
      return icons;
    },
  },
  methods: {
    selectPlan() {
      this.$emit("selected", this.plan);
    },
  },
});
</script>
