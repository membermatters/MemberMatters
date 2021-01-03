<template>
  <div class="q-pa-md">
    <q-card class="my-card">
      <div>
        <q-card-section>
          <div class="text-h6">{{ tier.name }}</div>
          <div class="text-subtitle2">{{ tier.description }}</div>
        </q-card-section>

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
  width: 300px;
  min-height: 300px;
}
</style>