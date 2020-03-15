<template>
  <q-page class="row flex content-start justify-center q-pt-xl">
    <report-issue-card />
  </q-page>
</template>

<script>
import ReportIssueCard from '../components/ReportIssueCard';

export default {
  name: 'ReportIssuePage',
  components: {
    ReportIssueCard,
  },
};
</script>
