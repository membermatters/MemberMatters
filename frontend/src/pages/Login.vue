<template>
  <q-page class="row flex content-start justify-center q-pt-xl">
    <login-card />
  </q-page>
</template>

<script>
import LoginCard from '../components/LoginCard';

export default {
  name: 'LoginPage',
  components: {
    LoginCard,
  },
};
</script>
