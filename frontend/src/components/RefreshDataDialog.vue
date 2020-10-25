<template>
  <q-dialog v-model="opened">
    <q-card>
      <q-card-section>
        <div class="text-h6">
          {{ $t('warning') }}
        </div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        {{ $t('dataRefreshWarning') }}
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          v-close-popup
          flat
          :label="$t('button.ok')"
          color="primary"
          @click="close"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: 'RefreshDataDialog',
  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      opened: false,
    };
  },
  created() {
    this.opened = value;
  },
  methods: {
    close() {
      this.$emit('input', false);
    },
  },
};
</script>
