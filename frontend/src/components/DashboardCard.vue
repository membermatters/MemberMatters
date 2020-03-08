<template>
  <div class="q-pa-md">
    <q-card class="my-card">
      <q-card-section>
        <div class="text-h6">
          {{ title }}
        </div>
      </q-card-section>

      <q-card-section>
        {{ description }}
      </q-card-section>

      <q-separator dark />

      <q-card-actions>
        <q-btn
          type="a"
          :href="linkLocation"
          flat
        >
          {{ linkText }}
        </q-btn>
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'DashboardCard',
  props: {
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    linkText: {
      type: String,
      required: true,
    },
    linkLocation: {
      type: String,
      required: true,
    },
  },
};
</script>
