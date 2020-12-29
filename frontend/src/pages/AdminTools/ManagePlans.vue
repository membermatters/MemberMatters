<template>
  <q-page class="column flex content-center justify-start">
    <member-tiers-lst/>
  </q-page>
</template>

<script lang="ts">
import MemberTiersList from '@components/AdminTools/MemberTiersList.vue';

export default {
  name: 'ManagePlans',
  components: { MemberTiersList },
  mounted() {
    let thing = 'lol';
  },
};
</script>
