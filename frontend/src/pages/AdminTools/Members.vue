<template>
  <q-page class="column flex content-center justify-start">
    <members-list />
  </q-page>
</template>

<script>
import MembersList from '@components/AdminTools/MembersList';

export default {
  name: 'MembersPage',
  components: { MembersList },
};
</script>
