<template>
  <q-page class="column flex items-center justify-center q-pt-xl">
    <template>
      <q-img
        contain
        src="../assets/img/logo/main-logo.png"
        class="header-image-mobile q-my-lg"
      />
    </template>

    <registration-card />
  </q-page>
</template>

<script>
import RegistrationCard from 'components/Account/RegistrationCard';

export default {
  name: 'RegistrationPage',
  components: {
    RegistrationCard,
  },
};
</script>

<style scoped>
  .header-image-mobile {
    max-height: 50px;
  }
</style>
