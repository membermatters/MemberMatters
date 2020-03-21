<template>
  <q-page class="row flex content-start justify-center">
    <div style="width: 100%;">
      <div
        class="row"
        style="width: 100%;"
      >
        <p class="q-px-lg q-pt-lg q-mb-none">
          {{ $t('memberGroups.pageDescription') }}
        </p>
      </div>
      <member-groups />
    </div>
  </q-page>
</template>

<script>
import MemberGroups from '../components/MemberGroups';

export default {
  name: 'MemberGroupsPage',
  components: { MemberGroups },
};
</script>
