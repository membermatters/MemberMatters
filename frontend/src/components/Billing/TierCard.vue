<template>
  <div class="q-pa-md">
    <q-card
      class="my-card shadow-5"
      :class="{ 'dark-border': $q.dark.isActive }"
    >
      <div style="min-height: 200px" class="column">
        <q-card-section>
          <div class="text-h6">{{ tier.name }}</div>
          <div class="text-subtitle2">{{ tier.description }}</div>
        </q-card-section>

        <q-space />

        <q-separator />

        <q-card-section>
          <div class="row justify-center">
            <q-btn color="primary" :label="$tc('button.select')" />
          </div>
        </q-card-section>
      </div>
    </q-card>
  </div>
</template>

<script lang="ts">
export default {
  name: "TierCard",
  props: {
    tier: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.my-card {
  min-width: 200px;
  min-height: 200px;
}

.dark-border {
  border: 1px solid;
}
</style>