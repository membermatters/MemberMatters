<template>
  <q-page class="column">
    <members-list />
  </q-page>
</template>

<script lang="ts">
import MembersList from '@components/AdminTools/MembersList.vue';

export default {
  name: 'MembersPage',
  components: { MembersList },
};
</script>
