<template>
  <q-card
    class="login-card"
  >
    <h6 class="q-ma-none q-pa-md">
      {{ $t('changePasswordCard.pageTitle') }}
    </h6>

    <q-card-section>
      <q-form
        class="q-gutter-md"
        @submit="onSubmit"
      >
        <q-input
          v-model="currentPassword"
          autofocus
          filled
          type="password"
          label="Current password"
          lazy-rules
          :rules="[
            val => validatePassword(val) || $t('validation.invalidPassword'),
          ]"
        />

        <q-input
          v-model="newPassword"
          filled
          type="password"
          label="New password"
          lazy-rules
          :rules="[
            val => validatePassword(val) || $t('validation.invalidPassword'),
          ]"
        />

        <q-input
          v-model="newPassword2"
          filled
          type="password"
          label="Confirm new password"
          lazy-rules
          :rules="[
            val => validatePassword(val) || $t('validation.invalidPassword'),
            val => validateMatchingField(val, newPassword) || $t('validation.passwordNotMatch'),
          ]"
        />

        <q-banner
          v-if="success"
          class="bg-positive text-white"
        >
          {{ $t('changePasswordCard.success') }}
        </q-banner>

        <q-banner
          v-if="error"
          class="bg-negative text-white"
        >
          {{ $t('changePasswordCard.fail') }}
        </q-banner>

        <div class="row">
          <q-space />
          <q-btn
            v-if="!success"
            :label="$t('button.submit')"
            type="submit"
            color="primary-btn"
            :loading="buttonLoading"
          />
          <q-btn
            v-if="success"
            v-close-popup
            :label="$t('button.close')"
            flat
          />
        </div>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import formMixin from '../mixins/formMixin';

export default {
  name: 'ChangePasswordCard',
  mixins: [formMixin],
  data() {
    return {
      currentPassword: '',
      newPassword: '',
      newPassword2: '',
      buttonLoading: false,
      error: false,
      success: false,
    };
  },
  methods: {
    onSubmit() {
      this.changePassword();
    },
    /**
     * This sends the API request to change the password.
     */
    changePassword() {
      this.fail = false;
      this.buttonLoading = true;

      this.$axios.put('/api/profile/password/', {
        current: this.currentPassword,
        new: this.newPassword,
      })
        .then((response) => {
          if (response.data.success === true) {
            this.error = false;
            this.success = true;
          } else {
            this.error = true;
          }
        })
        .catch((error) => {
          this.error = true;
          throw error;
        })
        .finally(() => {
          this.buttonLoading = false;
        });
    },
  },
};
</script>

<style scoped>
  .login-card {
    width: 320px;
  }
</style>
