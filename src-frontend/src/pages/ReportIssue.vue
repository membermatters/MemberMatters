<template>
  <q-page class="q-pt-md">
    <report-issue-card />
  </q-page>
</template>

<script>
import ReportIssueCard from '@components/ReportIssueCard.vue';

export default {
  name: 'ReportIssuePage',
  components: {
    ReportIssueCard,
  },
};
</script>
