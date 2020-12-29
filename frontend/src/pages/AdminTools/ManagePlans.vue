<template>
  <q-page class="column flex content-center justify-start">
    <plans-list />
  </q-page>
</template>

<script lang="ts">
import PlansList from '@components/AdminTools/PlansList.vue';

export default {
  name: 'ManagePlans',
  components: { PlansList },
  mounted() {
    let thing = 'lol';
  },
};
</script>
