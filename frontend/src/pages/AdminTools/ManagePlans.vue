<template>
  <q-page class="column flex content-center justify-start">
    <doors-list />
  </q-page>
</template>

<script lang="ts">
import DoorsList from '@components/AdminTools/DoorsList.vue';

export default {
  name: 'ManagePlans',
  components: { DoorsList },
  mounted() {
    let thing = 'lol';
  },
};
</script>
