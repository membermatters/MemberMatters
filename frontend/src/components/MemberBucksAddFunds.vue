<template>
  <q-dialog
    ref="dialog"
    @hide="onDialogHide"
  >
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <div class="text-h6">
          {{ $t('memberbucks.addFunds') }}
        </div>
        <div class="text-subtitle2">
          {{ $t('memberbucks.currentBalance') }} {{ $n(100, 'currency') }}
        </div>
      </q-card-section>

      <q-card-section>
        <q-btn
          :label="$n(10, 'currency')"
          color="primary"
        />
        <q-btn
          class="q-mx-sm"
          :label="$n(20, 'currency')"
          color="primary"
        />
        <q-btn
          :label="$n(30, 'currency')"
          color="primary"
        />
      </q-card-section>

      <q-card-section>
        <p>
          {{ $t('memberbucks.addFundsDescription') }}
        </p>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          color="primary"
          flat
          :label="$t('button.close')"
          @click="onCancelClick"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import icons from 'src/icons';

export default {
  name: 'MemberBucksAddFunds',
  props: {
    // ...your custom props
  },

  methods: {
    show() {
      this.$refs.dialog.show();
    },
    hide() {
      this.$refs.dialog.hide();
    },
    onDialogHide() {
      this.$emit('hide');
    },
    onOKClick() {
      this.$emit('ok');
      this.hide();
    },
    onCancelClick() {
      this.hide();
    },
  },
  computed: {
    icons() {
      return icons;
    },
  },
};
</script>
