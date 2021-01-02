<template>
  <q-page class="column flex content-center justify-start">
    <meetings-list />
  </q-page>
</template>

<script>
import MeetingsList from "../components/MeetingsList";

export default {
  name: "MeetingsPage",
  components: { MeetingsList },
};
</script>
