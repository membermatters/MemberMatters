<template>
  <div class="fixed-center text-center">
    <q-icon
      :name="icons.success"
      size="xl"
      color="success"
    />

    <br>
    <br>

    <p class="text-body1 text-faded">
      {{ $t('registrationCard.registrationComplete') }}
    </p>
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
  name: 'RegistrationSuccess',
  computed: {
    icons() {
      return icons;
    },
  },
};
</script>
