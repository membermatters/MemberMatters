<template>
  <q-page class="flex flex-center">
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
