<template>
  <q-page class="flex flex-start">
    <div>
      <h5 class="q-ma-md">
        Useful Resources
      </h5>
      <div class="row">
        <dashboard-card
          v-for="card in homepageCards"
          :key="card.linkLocation"
          class="col-12 col-sm-4"
          :title="card.title"
          :icon="card.icon"
          :description="card.description"
          :link-text="card.linkText"
          :link-location="card.linkLocation"
          :router-link="card.routerLink ? card.routerLink : false"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapGetters } from 'vuex';
import DashboardCard from '../components/DashboardCard';

export default {
  name: 'DashboardPage',
  components: { DashboardCard },
  computed: {
    ...mapGetters('config', ['homepageCards']),
  },
};
</script>

<style scoped>
  .row {
    width: 100%;
    max-width: 1200px;
    margin: auto;
  }
</style>
