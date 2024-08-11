<template>
  <q-card>
    <img :src="images.statsCard" />

    <q-list>
      <q-item>
        <q-item-section avatar>
          <q-icon color="primary" :name="icons.members" />
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ $t('statistics.memberCount') }}</q-item-label>
          <q-item-label caption>
            {{ onsiteCount }} {{ $t('statistics.on_site') }}
          </q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section avatar>
          <q-icon color="primary" :name="icons.membersOnSite" />
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ $t('statistics.memberList') }}</q-item-label>
          <q-item-label caption>
            {{ onsiteMembers.join(', ') }}
          </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import icons from '@icons';

export default {
  name: 'MembersOnsiteCard',
  data() {
    return {
      refreshInterval: null,
    };
  },
  mounted() {
    this.getSiteSignedIn();
    this.getStatistics();

    // Refresh statistics every 10 seconds while the page is open
    this.refreshInterval = setInterval(this.getStatistics, 10000);
  },
  beforeUnmount() {
    clearInterval(this.refreshInterval);
  },
  methods: {
    ...mapActions('profile', ['getSiteSignedIn']),
    ...mapActions('tools', ['getStatistics']),
  },
  computed: {
    ...mapGetters('config', ['images']),
    ...mapGetters('tools', ['statistics']),
    icons() {
      return icons;
    },
    onsiteCount() {
      return this.statistics?.on_site ? this.statistics?.on_site?.count : 0;
    },
    onsiteMembers() {
      return this.statistics?.on_site?.members
        ? this.statistics?.on_site?.members
        : [];
    },
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
