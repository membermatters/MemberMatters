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
        <q-btn
          v-else-if="linkLocation"
          :href="linkLocation"
          target="_blank"
          flat
        >
          {{ linkText }}
        </q-btn>
        <div v-else>
          <template :key="link.url" v-for="link in links">
            <q-btn :href="link.url" target="_blank" flat>
              {{ link.btn_text }}
            </q-btn>
            <q-separator v-if="link.newLine" vertical />
          </template>
        </div>
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
      required: false,
      default: null,
    },
    linkLocation: {
      type: [String, Object],
      required: false,
      default: null,
    },
    links: {
      type: Array,
      required: false,
      default: () => [],
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
