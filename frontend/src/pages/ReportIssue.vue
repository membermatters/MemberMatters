<template>
  <q-page class="q-pt-md">
    <report-issue-card />
  </q-page>
</template>

<script>
import ReportIssueCard from "../components/ReportIssueCard";

export default {
  name: "ReportIssuePage",
  components: {
    ReportIssueCard,
  },
};
</script>
