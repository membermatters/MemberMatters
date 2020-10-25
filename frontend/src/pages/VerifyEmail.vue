<template>
  <div class="fixed-center text-center">
    <template v-if="verifySuccess">
      <q-icon
        :name="icons.success"
        size="xl"
        color="success"
      />

      <br>
      <br>

      <p class="text-body1 text-faded">
        {{ $t('verifyEmail.complete') }}
      </p>
    </template>

    <template v-if="verifyError">
      <q-icon
        :name="icons.fail"
        size="xl"
        color="fail"
      />

      <br>
      <br>

      {{ $t('verifyEmail.error') }}
    </template>

    <br>
    <br>

    <q-btn
      color="primary-btn"
      style="width:200px;"
      to="/"
      label="Go Home"
    />
  </div>
</template>

<script>
import icons from '@icons';

export default {
  name: 'VerifyEmail',
  props: {
    verifyToken: {
      type: String,
      default: '',
    },
    verifySuccess: {
      type: Boolean,
      default: false,
    },
    verifyError: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    icons() {
      return icons;
    },
  },
  mounted() {
    this.$axios.post(`api/email/${this.verifyToken}/verify/`)
      .then(() => {
        /* eslint-disable */
        this.verifyError = false;
        this.verifySuccess = true;
        setTimeout(() => {
          this.$router.push({ name: 'dashboard' });
        }, 2000);
      })
      .catch(() => {
        this.verifyError = true;
        this.verifySuccess = false;
      });
  },
};
</script>
