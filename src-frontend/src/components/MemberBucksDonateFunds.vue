<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <div class="text-h6">
          {{ $t('memberbucks.donateFunds') }}
        </div>
        <div class="text-subtitle2">
          {{ $t('memberbucks.currentBalance') }} {{ balance }}
        </div>
      </q-card-section>

      <q-card-section>
        <q-input
          class="q-py-sm"
          prefix="$"
          outlined
          :disable="donatingFunds"
          v-model="amount"
          type="number"
          :label="$tc('memberbucks.totalAmount')"
          color="accent"
        />

        <q-input
          outlined
          :disable="donatingFunds"
          v-model="description"
          :label="$tc('form.description')"
          color="accent"
        />

        <q-btn
          @click="donateFunds()"
          class="q-mt-md"
          color="secondary"
          :icon-right="icons.submit"
          :label="$t('memberbucks.donateFunds')"
          :disable="donatingFunds || amount == 0"
        />
        <br />
        <q-spinner v-if="donatingFunds" color="primary" />
      </q-card-section>

      <q-card-section>
        <i18n-t keypath="memberbucks.donateFundsDescription" tag="p"></i18n-t>

        <q-banner v-if="donateFundsError" class="text-white bg-red">
          {{ donateFundsError }}
        </q-banner>

        <q-banner v-if="donateFundsSuccess" class="text-white bg-success">
          {{ $t('memberbucks.donateFundsSuccess') }}
        </q-banner>
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
import { defineComponent } from 'vue';
import icons from '@icons';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'MemberBucksDonateFunds',
  emits: ['ok', 'cancel', 'hide'],
  data() {
    return {
      donateFundsError: null,
      donateFundsSuccess: false,
      donatingFunds: false,
      amount: 0,
      description: '',
    };
  },
  methods: {
    ...mapActions('profile', ['getProfile']),
    ...mapActions('tools', [
      'getMemberBucksTransactions',
      'getMemberBucksBalance',
    ]),
    addFunds(amount) {
      this.amount += amount;
    },
    donateFunds() {
      this.donatingFunds = true;
      this.donateFundsSuccess = false;
      this.donateFundsError = false;
      let convertedAmount = Math.floor(this.amount * 100);
      this.$axios
        .post(`/api/memberbucks/pay/${convertedAmount}/`, {
          description: this.description,
        })
        .then(() => {
          this.getProfile();
          this.getMemberBucksTransactions();
          this.getMemberBucksBalance();
          this.donateFundsSuccess = true;
        })
        .catch(() => {
          this.donateFundsSuccess = false;
          this.donateFundsError = this.$t('memberbucks.donateFundsError');
        })
        .finally(() => {
          this.amount = 0;
          this.description = '';
          this.donatingFunds = false;
        });
    },
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
    ...mapGetters('config', ['siteLocaleCurrency']),
    icons() {
      return icons;
    },
    balance() {
      return this.$n(
        this?.profile?.financial?.memberBucks?.balance || 0,
        'currency',
        this.siteLocaleCurrency
      );
    },
  },
});
</script>
