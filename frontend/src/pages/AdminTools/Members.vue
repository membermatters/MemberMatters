<template>
  <q-page class="column flex content-center justify-start">
    <meetings-list />
  </q-page>
</template>

<script>
import MeetingsList from '@components/AdminTools/MembersList';

export default {
  name: 'MembersPage',
  components: { MeetingsList },
};
</script>
