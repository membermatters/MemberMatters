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

      <template v-if="profile.financial.memberBucks.savedCard.last4">
        <q-card-section>
          <q-btn
            :label="$n(10, 'currency')"
            color="accent"
          />
          <q-btn
            class="q-mx-sm"
            :label="$n(20, 'currency')"
            color="accent"
          />
          <q-btn
            :label="$n(30, 'currency')"
            color="accent"
          />
        </q-card-section>

        <q-card-section>
          <i18n
            path="memberbucks.addFundsDescription"
            tag="p"
          >
            <template v-slot:savedCard>
              <span class="proxy-field">
                <b>{{ profile.financial.memberBucks.savedCard.last4 }}</b>
              </span>
            </template>
          </i18n>
        </q-card-section>
      </template>

      <template v-else>
        <q-card-section>
          {{ $t('memberbucks.noSavedBilling') }}
        </q-card-section>
        <q-card-section>
          <q-btn
            color="accent"
            :icon="icons.billing"
            :label="$t('memberbucks.manageBilling')"
            @click="$router.push({ name: 'memberbucks', params: { dialog: 'billing' } })"
            class="q-mb-sm q-mr-md"
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
import icons from 'src/icons';
import { mapGetters } from 'vuex';

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
    ...mapGetters('profile', ['profile']),
    icons() {
      return icons;
    },
  },
};
</script>
