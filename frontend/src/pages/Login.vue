<template>
  <q-page class="row flex content-start justify-center q-pt-xl">
    <template>
      <q-img
        contain
        src="../assets/img/logo/logo-small.png"
        class="header-image-mobile q-my-lg"
      />
    </template>

    <login-card :reset-token="resetToken" />
  </q-page>
</template>

<script>
import LoginCard from '../components/LoginCard';

export default {
  name: 'LoginPage',
  components: {
    LoginCard,
  },
  props: {
    resetToken: {
      type: String,
      default: null,
    },
  },
};
</script>

<style scoped>
  .header-image-mobile {
    max-height: 50px;
  }
</style>
