<template>
  <q-dialog
    ref="dialog"
    @hide="onDialogHide"
  >
    <q-card class="q-dialog-plugin">
      <q-card-section>
        Hi
      </q-card-section>
      <q-card-actions align="right">
        <q-btn
          color="accent"
          flat
          :label="$t('button.close')"
          @click="onCancelClick"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: 'MemberBucksManageBilling',
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
};
</script>
