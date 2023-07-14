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

      <q-card-actions v-if="Platform.is.electron">
        <q-btn v-if="routerLink" :to="routerLink" flat>
          {{ linkText }}
        </q-btn>
        <q-btn v-else :href="linkLocation" target="_blank" flat>
          {{ linkLocation }}
        </q-btn>
      </q-card-actions>

      <q-card-actions v-else>
        <q-btn v-if="routerLink" :to="routerLink" flat>
          {{ linkText }}
        </q-btn>
        <q-btn v-else :href="linkLocation" target="_blank" flat>
          {{ linkText }}
        </q-btn>
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
import { Platform } from 'quasar';

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
      required: false,
      default: null,
    },
    routerLink: {
      type: [Object, Boolean],
      required: false,
      default: null,
    },
  },
  computed: {
    Platform() {
      return Platform;
    },
  },
};
</script>
