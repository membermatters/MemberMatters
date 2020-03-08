<template>
  <q-card class="my-card bg-secondary text-white">
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
      <q-btn flat>
        {{ linkText }}
      </q-btn>
    </q-card-actions>
  </q-card>
</template>

<script>
export default {
  name: 'HomePageCard',
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
  },
};
</script>
