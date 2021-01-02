<template>
  <q-page class="column">
    <members-list />
  </q-page>
</template>

<script>
import MembersList from "@components/AdminTools/MembersList";

export default {
  name: "MembersPage",
  components: { MembersList },
};
</script>
