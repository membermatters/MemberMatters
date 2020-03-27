<template>
  <div class="profile-form">
    <q-input
      outlined
      v-model="text"
      label="Name"
    />
  </div>
</template>

<script>
import icons from '../icons';

export default {
  name: 'ProfileForm',
  computed: {
    icons() {
      return icons;
    },
  },
};
</script>
