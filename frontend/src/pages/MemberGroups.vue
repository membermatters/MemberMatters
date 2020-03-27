<template>
  <q-page class="column flex content-center justify-start">
    <p>
      {{ $t('memberGroups.pageDescription') }}
    </p>
    <member-groups />
  </q-page>
</template>

<script>
import MemberGroups from '../components/MemberGroups';

export default {
  name: 'MemberGroupsPage',
  components: { MemberGroups },
};
</script>
