<template>
  <q-page class="row flex content-start justify-center">
    <div v-if="loggedIn">
      <div class="column flex content-start justify-center">
        <q-banner
          v-if="profile.lastInduction === null"
          inline-actions
          rounded
          class="bg-red text-white q-ma-md"
        >
          <template v-slot:avatar>
            <q-icon :name="icons.warning" />
          </template>
          <div v-if="profile.inductionLink.length != 0">
            {{ $t('access.inductionIncompleteTasks') }}
            <li v-for="(link, index) in profile.inductionLink" :key="index">
              <a :href="link" target="_blank">Task {{ index+1 }}</a>
            </li>
          </div>
          <div v-else>{{ $t('access.inductionIncompleteNoTasks') }}</div>
        </q-banner>

        <q-banner
          v-if="
            profile.memberStatus !== 'active' &&
            profile.memberStatus !== 'accountonly'
          "
          inline-actions
          rounded
          class="bg-orange text-white q-ma-md"
        >
          <template v-slot:avatar>
            <q-icon :name="icons.warning" />
          </template>
          {{ $t('access.inactive') }}
        </q-banner>
      </div>

      <h5 class="q-ma-md">
        {{ $t('dashboard.quickCards') }}
      </h5>
      <div class="row">
        <quick-cards />
      </div>

      <h5 class="q-ma-md">
        {{ $t('dashboard.usefulResources') }}
      </h5>
      <div class="row flex items-stretch justify-start">
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
          :links="card.links"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import QuickCards from '@components/QuickCards.vue';
import { Platform } from 'quasar';
import DashboardCard from '@components/DashboardCard.vue';
import icons from 'src/icons';

export default {
  name: 'DashboardPage',
  components: { QuickCards, DashboardCard },
  computed: {
    Platform() {
      return Platform;
    },
    ...mapGetters('config', ['homepageCards', 'features']),
    ...mapGetters('profile', ['loggedIn', 'profile']),
    icons() {
      return icons;
    },
  },
  methods: {
    ...mapActions('profile', ['getProfile']),
  },
  async mounted() {
    await this.getProfile();
    if (
      this.profile.memberStatus === 'noob' &&
      this.$route.name !== 'membershipPlan' &&
      this.features.enableMembershipPayments
    ) {
      this.$router.push({ name: 'membershipPlan' });
    }
  },
};
</script>

<style lang="sass" scoped>
.row
  width: 100%
  max-width: $maxWidth
  margin: auto
</style>
