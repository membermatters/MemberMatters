<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <div class="text-h6">
          {{ $t("memberbucks.donateFunds") }}
        </div>
        <div class="text-subtitle2">
          {{ $t("memberbucks.currentBalance") }} {{ balance }}
        </div>
      </q-card-section>

      <q-card-section>
        <div class="text-subtitle2 q-pb-sm">
          {{ $t("memberbucks.quickAdd") }}
        </div>
        <q-btn
          :disable="donatingFunds"
          class="q-mr-sm"
          :label="$n(0.5, 'currency')"
          color="accent"
          @click="addFunds(0.5)"
        />
        <q-btn
          :disable="donatingFunds"
          class="q-mr-sm"
          :label="$n(1, 'currency')"
          color="accent"
          @click="addFunds(1)"
        />
        <q-btn
          :disable="donatingFunds"
          class="q-mr-sm"
          :label="$n(2, 'currency')"
          color="accent"
          @click="addFunds(2)"
        /><q-btn
          :disable="donatingFunds"
          :label="$n(3, 'currency')"
          color="accent"
          @click="addFunds(3)"
        />

        <q-input
          class="q-py-sm"
          prefix="$"
          outlined
          :disable="donatingFunds"
          v-model="amount"
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
        <i18n path="memberbucks.donateFundsDescription" tag="p"></i18n>

        <q-banner v-if="donateFundsError" class="text-white bg-red">
          {{ donateFundsError }}
        </q-banner>

        <q-banner v-if="donateFundsSuccess" class="text-white bg-success">
          {{ $t("memberbucks.donateFundsSuccess") }}
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
import icons from "@icons";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "MemberBucksDonateFunds",
  emits: ["ok", "cancel"],
  data() {
    return {
      donateFundsError: null,
      donateFundsSuccess: false,
      donatingFunds: false,
      amount: 0,
      description: "",
    };
  },
  methods: {
    ...mapActions("profile", ["getProfile"]),
    ...mapActions("tools", [
      "getMemberBucksTransactions",
      "getMemberBucksBalance",
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
        .post(`/api/memberbucks/donate/${convertedAmount}/`, {
          description: this.description,
        })
        .then(() => {
          this.getProfile();
          this.getMemberBucksTransactions();
          this.getMemberBucksBalance();
          this.donateFundsSuccess = true;
        })
        .catch(() => {
          console.log("help");
          this.donateFundsSuccess = false;
          this.donateFundsError = this.$t("memberbucks.donateFundsError");
        })
        .finally(() => {
          this.amount = 0;
          this.description = "";
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
      this.$emit("hide");
    },
    onOKClick() {
      this.$emit("ok");
      this.hide();
    },
    onCancelClick() {
      this.hide();
    },
  },
  computed: {
    ...mapGetters("profile", ["profile"]),
    icons() {
      return icons;
    },
    balance() {
      return this.$n(
        this?.profile?.financial?.memberBucks?.balance,
        "currency"
      );
    },
  },
};
</script>
