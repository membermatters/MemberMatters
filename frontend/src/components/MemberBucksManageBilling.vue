<template>
  <q-dialog
    ref="dialog"
    @hide="onDialogHide"
  >
    <q-card class="q-dialog-plugin">
      <template v-if="profile.financial.memberBucks.savedCard.last4">
        <q-card-section>
          {{ $t('memberbucks.savedCard') }}
        </q-card-section>

        <q-card-section>
          <credit-card
            :name="profile.fullName"
            :expiry="profile.financial.memberBucks.savedCard.expiry"
            :last4="profile.financial.memberBucks.savedCard.last4"
            :brand="profile.financial.memberBucks.savedCard.brand"
            class="shadow-7"
          />
        </q-card-section>
      </template>

      <template v-else>
        <member-bucks-add-card />
      </template>

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
import CreditCard from 'components/CreditCard';
import { mapGetters } from 'vuex';
import MemberBucksAddCard from 'components/MemberBucksAddCard';

export default {
  name: 'MemberBucksManageBilling',
  components: { MemberBucksAddCard, CreditCard },
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
    ...mapGetters('profile', ['profile']),
  },
};
</script>
