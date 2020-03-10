<template>
  <q-page class="flex flex-center">
    <div class="row">
      <dashboard-card
        class="col-12 col-sm-4"
        title="HSBNE Wiki"
        description="Our wiki is like the rule book for HSBNE. It contains all the information abt."
        link-text="Read Wiki"
        link-location="https://wiki.hsbne.org/"
      />
    </div>
  </q-page>
</template>

<script>
import DashboardCard from '../components/DashboardCard';

export default {
  name: 'DashboardPage',
  components: { DashboardCard },
};
</script>
