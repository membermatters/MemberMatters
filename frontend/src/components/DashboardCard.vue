<template>
  <div class="q-pa-md">
    <q-card class="my-card">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon :name="icon" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ title }}</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section>
        {{ description }}
      </q-card-section>

      <q-separator dark />

      <q-card-actions>
        <q-btn
          v-if="routerLink"
          :to="linkLocation"
          flat
        >
          {{ linkText }}
        </q-btn>
        <q-btn
          v-else
          type="a"
          :href="linkLocation"
          target="_blank"
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
    icon: {
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
      type: [String, Object],
      required: true,
    },
    routerLink: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
