<template>
  <q-page class="row flex content-start justify-center">
    <div v-if="loggedIn">
      <h5 class="q-ma-md">
        Useful Resources
      </h5>
      <div class="row">
        <dashboard-card
          v-for="card in homepageCards"
          :key="card.title"
          class="col-12 col-sm-4"
          :title="card.title"
          :icon="card.icon"
          :description="card.description"
          :link-text="card.btn_text"
          :link-location="card.url"
          :router-link="card.routerLink ? card.routerLink : false"
        />
      </div>
    </div>
    <div v-else />
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
    ...mapGetters('profile', ['loggedIn']),
  },
};
</script>

<style lang="sass" scoped>
  .row
    width: 100%
    max-width: $maxWidth
    margin: auto
</style>
