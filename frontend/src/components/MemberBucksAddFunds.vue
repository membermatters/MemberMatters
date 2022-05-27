<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <div class="text-h6">
          {{ $t("memberbucks.addFunds") }}
        </div>
        <div class="text-subtitle2">
          {{ $t("memberbucks.currentBalance") }} {{ balance }}
        </div>
      </q-card-section>

      <template v-if="profile?.financial?.memberBucks?.savedCard?.last4">
        <q-card-section>
          <i18n-t keypath="memberbucks.addFundsDescription" tag="p">
            <template v-slot:savedCard>
              <span class="proxy-field">
                <b>{{ profile?.financial?.memberBucks?.savedCard?.last4 }}</b>
              </span>
            </template>
          </i18n-t>

          <q-banner v-if="addFundsError" class="text-white bg-red">
            {{ addFundsError }}
          </q-banner>
          <q-banner v-if="addFundsSuccess" class="text-white bg-success">
            {{ $t("memberbucks.addFundsSuccess") }}
          </q-banner>
        </q-card-section>

        <q-card-section>
          <q-btn
            :disable="addingFunds"
            :label="$n(10, 'currency')"
            color="accent"
            @click="addFunds(10)"
          />
          <q-btn
            :disable="addingFunds"
            class="q-mx-sm"
            :label="$n(20, 'currency')"
            color="accent"
            @click="addFunds(20)"
          />
          <q-btn
            :disable="addingFunds"
            :label="$n(30, 'currency')"
            color="accent"
            @click="addFunds(30)"
          />
          <br />
          <q-spinner v-if="addingFunds" color="primary" />
        </q-card-section>
      </template>

      <template v-else>
        <q-card-section>
          {{ $t("memberbucks.noSavedBilling") }}
        </q-card-section>
        <q-card-section>
          <q-btn
            color="accent"
            :icon="icons.billing"
            :label="$t('memberbucks.manageBilling')"
            class="q-mb-sm q-mr-md"
            @click="
              $router.push({
                name: 'billing',
              })
            "
          />
        </q-card-section>
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
import icons from "@icons";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "MemberBucksAddFunds",
  emits: ["ok", "cancel", "hide"],
  data() {
    return {
      addFundsError: null,
      addFundsSuccess: false,
      addingFunds: false,
    };
  },
  methods: {
    ...mapActions("profile", ["getProfile"]),
    ...mapActions("tools", [
      "getMemberBucksTransactions",
      "getMemberBucksBalance",
    ]),
    addFunds(amount) {
      this.addingFunds = true;
      this.addFundsSuccess = false;
      this.addFundsError = false;
      this.$axios
        .post(`/api/memberbucks/add/${amount}/`)
        .then(() => {
          this.getProfile();
          this.getMemberBucksTransactions();
          this.getMemberBucksBalance();
          this.addFundsSuccess = true;
        })
        .catch(() => {
          this.addFundsError = this.$t("memberbucks.addCardError");
        })
        .finally(() => {
          this.addingFunds = false;
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
        this?.profile?.financial?.memberBucks?.balance || 0,
        "currency"
      );
    },
  },
};
</script>
