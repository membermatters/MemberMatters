<template>
  <q-page class="column flex items-center justify-center q-pt-xl">
    <template>
      <q-img
        contain
        :src="images.siteLogo"
        class="header-image-mobile q-my-lg"
      />
    </template>

    <registration-card />
  </q-page>
</template>

<script lang="ts">
import RegistrationCard from '@components/Account/RegistrationCard.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'RegistrationPage',
  components: {
    RegistrationCard,
  },
  computed: {
    ...mapGetters('config', ['images']),
  },
};
</script>

<style scoped>
.header-image-mobile {
  max-height: 50px;
}
</style>
