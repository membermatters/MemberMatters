<template>
  <q-page class="column flex content-center justify-start">
    <p class="text-body1">
      {{ $t('memberGroups.pageDescription') }}
    </p>
    <member-groups />
  </q-page>
</template>

<script>
import MemberGroups from "../components/MemberGroups";

export default {
  name: "MemberGroupsPage",
  components: { MemberGroups },
};
</script>
